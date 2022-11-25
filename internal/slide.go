package internal

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"time"
)

type Slide struct {
	Name           string                 `json:"name" yaml:"name"`
	Type           string                 `json:"type" yaml:"type"`
	DurationAmount string                 `json:"duration" yaml:"duration"`
	Duration       time.Duration          `json:"-" yaml:"-"`
	Params         map[string]interface{} `json:"params" yaml:"params"`
}

func (s *Slide) Validate() error {
	if s.Name == "" {
		return errors.New("slide name cannot be empty")
	}

	if s.Type == "" {
		return errors.New("slide type cannot be empty")
	}

	if s.DurationAmount == "" {
		return errors.New("slide duration cannot be empty")
	}

	duration, err := time.ParseDuration(s.DurationAmount)
	if err != nil {
		return fmt.Errorf("slide duration is invalid: %s", s.DurationAmount)
	}
	s.Duration = duration
	return nil
}

func (s *Slide) GetImage(config *Config, screen *ScreenSize) (string, error) {
	imagePath := filepath.Join(config.ImagesPath, s.Name+".png")
	_, err := os.Stat(imagePath)
	if os.IsNotExist(err) {
		return s.GenerateImage(config, screen)
	} else if err != nil {
		return "", err
	}
	return imagePath, nil
}

func (s *Slide) GenerateImage(config *Config, screen *ScreenSize) (string, error) {
	imageSource := config.ImageSources.Get(s.Type)
	if imageSource == nil {
		return "", fmt.Errorf("no image source found for type \"%s\"", s.Type)
	}

	generatedImage := filepath.Join(config.ImagesPath, s.Name+".png")
	err := imageSource.GenerateToFile(s.Name, generatedImage, screen.Width, screen.Height, s.Params)
	return generatedImage, err
}
