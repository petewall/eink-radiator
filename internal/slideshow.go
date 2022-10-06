package internal

import (
	"fmt"
	"time"

	"github.com/sirupsen/logrus"
)

type Slideshow struct {
	SlideConfig *SlideConfig
	slideIndex  int

	Screen Screen

	ToolsPath string
	ImagePath string

	Logger *logrus.Logger
}

func (s *Slideshow) Start() {
	s.slideIndex = 0

	for {
		slide := s.SlideConfig.Slides[s.slideIndex]
		s.slideIndex = (s.slideIndex + 1) % len(s.SlideConfig.Slides)

		image, err := slide.GenerateImage(s.ToolsPath, s.ImagePath, s.Screen.GetSize())
		if err != nil {
			s.Logger.WithError(err).Warn(fmt.Sprintf("slide %d (%s) failed to generate an image, skipping", s.slideIndex, slide.Name))
			continue
		}

		err = s.Screen.SetImage(image)
		if err != nil {
			s.Logger.WithError(err).Warn(fmt.Sprintf("failed to display slide %d (%s), skipping", s.slideIndex, slide.Name))
			continue
		}

		duration, err := time.ParseDuration(slide.Duration)
		if err != nil {
			s.Logger.WithError(err).Warn(fmt.Sprintf("slide %d (%s) has an invalid duration %s, skipping", s.slideIndex, slide.Name, slide.Duration))
			continue
		}

		time.Sleep(duration)
	}
}
