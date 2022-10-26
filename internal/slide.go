package internal

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"time"

	"gopkg.in/yaml.v3"
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
	tool := config.GetTool(s.Type)
	if tool == nil {
		return "", fmt.Errorf("no tool found for type \"%s\"", s.Type)
	}

	slideConfig, err := yaml.Marshal(s.Params)
	if err != nil {
		return "", fmt.Errorf("failed to prepare slide config: %w", err)
	}

	file, err := TempFile(s.Name+"-"+s.Type+"-config-*.yaml", slideConfig)
	if err != nil {
		return "", fmt.Errorf("failed to write slide config: %w", err)
	}

	// Need to do the anonymous function to appease the errcheck linter.
	// Since defer doesn't handle return values, and we need to explicitly
	// state that we're disregarding the error return value of RemoveFile
	defer func() { _ = RemoveFile(file.Name()) }()

	generatedImage := filepath.Join(config.ImagesPath, s.Name+".png")
	args := []string{
		"generate",
		"--config", file.Name(),
		"--height", strconv.Itoa(screen.Height),
		"--width", strconv.Itoa(screen.Width),
		"--output", generatedImage,
	}
	session := ExecCommand(tool.Path, args...)
	err = session.Run()
	if err != nil {
		return "", fmt.Errorf("image generator failed: %w", err)
	}
	return generatedImage, nil
}
