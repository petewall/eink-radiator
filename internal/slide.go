package internal

import (
	"fmt"
	"os"
	"path/filepath"
	"strconv"

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
		return fmt.Errorf("unexpected slide config kind: %s", sc.APIVersion)
	}

	return nil
}

type Slide struct {
	Type     string                 `json:"type" yaml:"type"`
	Name     string                 `json:"name" yaml:"name"`
	Duration string                 `json:"duration" yaml:"duration"`
	Params   map[string]interface{} `json:"params" yaml:"params"`
}

func (s *Slide) GenerateImage(tool *Tool, imageDir string, screen *ScreenSize) (string, error) {
	slideConfig, err := yaml.Marshal(s.Params)
	if err != nil {
		return "", fmt.Errorf("failed to prepare slide config: %w", err)
	}

	file, err := os.CreateTemp("", s.Name+"-"+s.Type+"-config-*.yaml")
	_, err = file.Write(slideConfig)
	if err != nil {
		return "", fmt.Errorf("failed to write slide config: %w", err)
	}
	defer os.Remove(file.Name())

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
