package internal

import (
	"encoding/json"
	"fmt"
	"path/filepath"
)

type ScreenSize struct {
	Height int `json:"height"`
	Width  int `json:"width"`
}

type Screen struct {
	Kind    string      `json:"kind"`
	Size    *ScreenSize `json:"size"`
	Palette []string    `json:"palette"`
	Path    string      `json:"-"`
}

func LoadFromDriver(screenPath string) (*Screen, error) {
	output, err := ExecCommand(screenPath, "config").Output()
	if err != nil {
		return nil, fmt.Errorf("failed to get screen config from %s: %w", screenPath, err)
	}

	var screen *Screen
	err = json.Unmarshal(output, &screen)
	if err != nil {
		return nil, fmt.Errorf("failed to parse screen config from %s: %w", screenPath, err)
	}
	screen.Path = screenPath

	return screen, nil
}

func (s *Screen) SetImage(config *Config, imagePath string) error {
	args := []string{"display", imagePath, "--save", filepath.Join(config.ImagesPath, "screen.png")}
	session := ExecCommand(s.Path, args...)
	err := session.Run()
	if err != nil {
		return fmt.Errorf("failed to display the image %s: %w", imagePath, err)
	}
	return nil
}
