package internal

import (
	"fmt"
	"path/filepath"
	"strconv"
	"strings"
)

const (
	SlideConfigAPIVersion = "v1.eink-radiator.petewall.net"
	SlideConfigKind       = "Slides"
)

type SlideConfig struct {
	APIVersion string   `json:"apiVersion"`
	Kind       string   `json:"kind"`
	Slides     []*Slide `json:"slides"`
}

type SlideConfigFileParser func(path string) (*SlideConfig, error)

var ParseSlideConfigFromFile = func(path string) (*SlideConfig, error) {
	return &SlideConfig{
		Slides: []*Slide{
			{
				Type:     "blank",
				Name:     "Red",
				Duration: "1s",
				Params: map[string]interface{}{
					"color": "red",
				},
			},
			{
				Type:     "blank",
				Name:     "Black",
				Duration: "1s",
				Params: map[string]interface{}{
					"color": "black",
				},
			},
			{
				Type:     "blank",
				Name:     "White",
				Duration: "1s",
				Params: map[string]interface{}{
					"color": "white",
				},
			},
		},
	}, nil
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
	Type     string                 `json:"type"`
	Name     string                 `json:"name,omitempty"`
	Duration string                 `json:"duration"`
	Params   map[string]interface{} `json:"params"`
}

func (s *Slide) GenerateImage(toolsPath, imagePath string, screen *ScreenSize) (string, error) {
	cmd := filepath.Join(toolsPath, s.Type)
	args := []string{"generate", "--height", strconv.Itoa(screen.Height), "--width", strconv.Itoa(screen.Width)}
	fmt.Printf("running %s %s\n", cmd, strings.Join(args, " "))
	// session := exec.Command(s.Type, "--height", strconv.Itoa(screen.Height), "--width", strconv.Itoa(screen.Width))
	// err := session.Run()
	return "", nil
}
