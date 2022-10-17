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

//counterfeiter:generate . SlideshowAPI
type SlideshowAPI interface {
	NextSlide()
	PreviousSlide()
}

type Slideshow struct {
	Config      *Config
	SlideConfig *SlideConfig
	slideIndex  int

	Screen Screen
	Logger *logrus.Logger

	actionChan chan string
}

func (s *Slideshow) Start() {
	s.slideIndex = 0
	s.actionChan = make(chan string, 5) // Why 5? i dunno. test with multiple actions and see if this makes sense

	for {
		slide := s.SlideConfig.Slides[s.slideIndex]

		s.DisplaySlide(slide)

		select {
		case action := <-s.actionChan:
			s.Logger.Debugf("action requested: %s", action)
			if action == SlideshowActionPrevious {
				s.slideIndex = (s.slideIndex - 2 + len(s.SlideConfig.Slides)) % len(s.SlideConfig.Slides)
			} else if action == SlideshowActionStop {
				break
			}
		case <-time.After(slide.Duration):
			s.Logger.Debug("sleeping complete")
		}

		s.slideIndex = (s.slideIndex + 1) % len(s.SlideConfig.Slides)
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

func (s *Slideshow) DisplaySlide(slide *Slide) {
	s.Logger.Debugf("generating image for slide %d (%s)...", s.slideIndex, slide.Name)

	tool := s.Config.GetTool(slide.Type)
	if tool == nil {
		s.Logger.Warn(fmt.Sprintf("slide %d (%s) uses an unknown tool type (%s), skipping", s.slideIndex, slide.Name, slide.Type))
		return
	}

	image, err := slide.GenerateImage(tool, s.Config.ImagesPath, s.Screen.GetSize())
	if err != nil {
		s.Logger.WithError(err).Warn(fmt.Sprintf("slide %d (%s) failed to generate an image, skipping", s.slideIndex, slide.Name))
		return
	}
	s.Logger.Debugf("finished generating image for slide %d (%s): %s", s.slideIndex, slide.Name, image)

	s.Logger.Debugf("displaying image for slide %d (%s)...", s.slideIndex, slide.Name)
	err = s.Screen.SetImage(image)
	if err != nil {
		s.Logger.WithError(err).Warn(fmt.Sprintf("failed to display slide %d (%s), skipping", s.slideIndex, slide.Name))
		return
	}
	s.Logger.Debugf("finished displaying image for slide %d (%s)", s.slideIndex, slide.Name)
}
