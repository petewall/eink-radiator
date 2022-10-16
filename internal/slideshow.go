package internal

import (
	"fmt"
	"time"

	"github.com/sirupsen/logrus"
)

type Slideshow struct {
	Config      *Config
	SlideConfig *SlideConfig
	slideIndex  int

	Screen Screen
	Logger *logrus.Logger
}

func (s *Slideshow) Start() {
	s.slideIndex = 0

	for {
		slide := s.SlideConfig.Slides[s.slideIndex]
		s.DisplaySlide(slide)
		s.slideIndex = (s.slideIndex + 1) % len(s.SlideConfig.Slides)
	}
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

	duration, err := time.ParseDuration(slide.Duration)
	s.Logger.Debugf("sleeping for %s...", duration.String())
	if err != nil {
		s.Logger.WithError(err).Warn(fmt.Sprintf("slide %d (%s) has an invalid duration %s, skipping", s.slideIndex, slide.Name, slide.Duration))
		return
	}

	time.Sleep(duration)
}
