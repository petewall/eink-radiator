package internal

import (
	"fmt"

	"github.com/petewall/eink-radiator/v2/pkg"
)

type Config struct {
	APIVersion   string           `json:"apiVersion" yaml:"apiVersion" `
	Kind         string           `json:"kind" yaml:"kind"`
	ImageSources pkg.ImageSources `json:"imageSources" yaml:"imageSources"`
	ImagesPath   string           `json:"imagesPath" yaml:"imagesPath"`
	ScreenPath   string           `json:"screenPath" yaml:"screenPath"`
	SlidesPath   string           `json:"slidesPath" yaml:"slidesPath"`
	Port         int              `json:"port" yaml:"port"`
}

type Tool struct {
	Name string `json:"name" yaml:"name"`
	Path string `json:"path" yaml:"path"`
}

const (
	ConfigAPIVersion = "v1.eink-radiator.petewall.net"
	ConfigKind       = "Config"
)

func (c *Config) Validate() error {
	if c.APIVersion != ConfigAPIVersion {
		return fmt.Errorf("unexpected config API version: %s", c.APIVersion)
	}

	if c.Kind != ConfigKind {
		return fmt.Errorf("unexpected config kind: %s", c.Kind)
	}

	return nil
}
