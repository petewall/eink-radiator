package internal

import (
	"errors"
	"fmt"
	"path/filepath"
	"strconv"
	"time"

	"gopkg.in/yaml.v3"
)

const (
	SlideConfigAPIVersion = "v1.eink-radiator.petewall.net"
	SlideConfigKind       = "Slides"
)

type SlideConfig struct {
	APIVersion string   `json:"apiVersion" yaml:"apiVersion"`
	Kind       string   `json:"kind" yaml:"kind"`
	Slides     []*Slide `json:"slides" yaml:"slides"`
}

func (sc *SlideConfig) Validate() error {
	if sc.APIVersion != SlideConfigAPIVersion {
		return fmt.Errorf("unexpected slide config API version: %s", sc.APIVersion)
	}

	if sc.Kind != SlideConfigKind {
		return fmt.Errorf("unexpected slide config kind: %s", sc.Kind)
	}

	if len(sc.Slides) == 0 {
		return errors.New("slide config does not contain any slides")
	}

	slideIndecies := map[string]int{}
	for slideIndex, slide := range sc.Slides {
		existingSlideIndex, isPresent := slideIndecies[slide.Name]
		if isPresent {
			return fmt.Errorf("slide #%d (%s) has the same name as the earlier slide #%d", slideIndex, slide.Name, existingSlideIndex)
		}
		slideIndecies[slide.Name] = slideIndex
		err := slide.Validate()
		if err != nil {
			return fmt.Errorf("slide #%d (%s) is not valid: %w", slideIndex, slide.Name, err)
		}
	}

	return nil
}

type Slide struct {
	Name     string                 `json:"name" yaml:"name"`
	Type     string                 `json:"type" yaml:"type"`
	Duration string                 `json:"duration" yaml:"duration"`
	Params   map[string]interface{} `json:"params" yaml:"params"`
}

func (s *Slide) Validate() error {
	if s.Name == "" {
		return errors.New("slide name cannot be empty")
	}

	if s.Type == "" {
		return errors.New("slide type cannot be empty")
	}

	if s.Duration == "" {
		return errors.New("slide duration cannot be empty")
	}

	_, err := time.ParseDuration(s.Duration)
	if err != nil {
		return fmt.Errorf("slide duration is invalid: %s", s.Duration)
	}
	return nil
}

func (s *Slide) GenerateImage(tool *Tool, imageDir string, screen *ScreenSize) (string, error) {
	slideConfig, err := yaml.Marshal(s.Params)
	if err != nil {
		return "", fmt.Errorf("failed to prepare slide config: %w", err)
	}

	file, err := TempFile(s.Name+"-"+s.Type+"-config-*.yaml", slideConfig)
	if err != nil {
		return "", fmt.Errorf("failed to write slide config: %w", err)
	}
	defer RemoveFile(file.Name())

	generatedImage := filepath.Join(imageDir, s.Name+".png")
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
