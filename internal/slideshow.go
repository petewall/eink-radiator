package internal

import (
	"fmt"
	"time"

	"github.com/sirupsen/logrus"
)

const (
	SlideshowActionNext     = "next"
	SlideshowActionPrevious = "previous"
	SlideshowActionStop     = "stop"
)

//go:generate go run github.com/maxbrunsfeld/counterfeiter/v6 . SlideshowAPI
type SlideshowAPI interface {
	GetSlide(name string) *Slide
	GetSlideConfig() *SlideConfig
	Start()
	Stop()
	NextSlide()
	PreviousSlide()
}

type Slideshow struct {
	config     *Config
	slides     *SlideConfig
	screen     *Screen
	log        *logrus.Logger
	actionChan chan string
}

func NewSlideshow(config *Config, slides *SlideConfig, screen *Screen, log *logrus.Logger) SlideshowAPI {
	return &Slideshow{
		config:     config,
		slides:     slides,
		screen:     screen,
		log:        log,
		actionChan: make(chan string, 5), // Why 5? i dunno. test with multiple actions and see if this makes sense
	}
}

func (s *Slideshow) GetSlide(name string) *Slide {
	for _, slide := range s.slides.Slides {
		if slide.Name == name {
			return slide
		}
	}
	return nil
}

func (s *Slideshow) GetSlideConfig() *SlideConfig {
	return s.slides
}

func (s *Slideshow) Start() {
	slideIndex := 0

	for {
		slide := s.slides.Slides[slideIndex]

		s.log.Debugf("generating image for slide %d (%s)...", slideIndex, slide.Name)
		tool := s.config.GetTool(slide.Type)
		if tool == nil {
			s.log.Warn(fmt.Sprintf("slide %d (%s) uses an unknown tool type (%s), skipping", slideIndex, slide.Name, slide.Type))
			return
		}

		image, err := slide.GenerateImage(tool, s.config.ImagesPath, s.screen.Size)
		if err != nil {
			s.log.WithError(err).Warn(fmt.Sprintf("slide %d (%s) failed to generate an image, skipping", slideIndex, slide.Name))
			return
		}
		s.log.Debugf("finished generating image for slide %d (%s): %s", slideIndex, slide.Name, image)

		s.log.Debugf("displaying image for slide %d (%s)...", slideIndex, slide.Name)
		err = s.screen.SetImage(image)
		if err != nil {
			s.log.WithError(err).Warn(fmt.Sprintf("failed to display slide %d (%s), skipping", slideIndex, slide.Name))
			return
		}
		s.log.Debugf("finished displaying image for slide %d (%s)", slideIndex, slide.Name)

		select {
		case action := <-s.actionChan:
			s.log.Debugf("action requested: %s", action)
			if action == SlideshowActionPrevious {
				slideIndex = (slideIndex - 2 + len(s.slides.Slides)) % len(s.slides.Slides)
			} else if action == SlideshowActionStop {
				return
			}
		case <-time.After(slide.Duration):
			s.log.Debug("sleeping complete")
		}

		slideIndex = (slideIndex + 1) % len(s.slides.Slides)
	}
}

func (s *Slideshow) NextSlide() {
	s.actionChan <- SlideshowActionNext
}

func (s *Slideshow) PreviousSlide() {
	s.actionChan <- SlideshowActionPrevious
}

func (s *Slideshow) Stop() {
	s.actionChan <- SlideshowActionStop
}
