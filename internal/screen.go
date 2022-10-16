package internal

import (
	"encoding/json"
	"fmt"
)

type ScreenSize struct {
	Height int `json:"height"`
	Width  int `json:"width"`
}

type Screen interface {
	GetSize() *ScreenSize
	GetPalette() []string
	SetImage(imagePath string) error
}

type ScreenDriver struct {
	Size    *ScreenSize `json:"size"`
	Palette []string    `json:"palette"`
	Path    string      `json:"-"`
}

func LoadFromDriver(screenPath string) (Screen, error) {
	output, err := ExecCommand(screenPath, "config").Output()
	if err != nil {
		return nil, fmt.Errorf("failed to get screen config from %s: %w", screenPath, err)
	}

	var driver *ScreenDriver
	err = json.Unmarshal(output, &driver)
	if err != nil {
		return nil, fmt.Errorf("failed to parse screen config from %s: %w", screenPath, err)
	}
	driver.Path = screenPath

	return driver, nil
}

func (s *ScreenDriver) GetSize() *ScreenSize {
	return s.Size
}

func (s *ScreenDriver) GetPalette() []string {
	return s.Palette
}

func (s *ScreenDriver) SetImage(imagePath string) error {
	args := []string{"display", imagePath}
	session := ExecCommand(s.Path, args...)
	err := session.Run()
	if err != nil {
		return fmt.Errorf("failed to display the image %s: %w", imagePath, err)
	}
	return nil
}
