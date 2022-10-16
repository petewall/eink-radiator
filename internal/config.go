package internal

import "fmt"

type Config struct {
	APIVersion string  `json:"apiVersion" yaml:"apiVersion" `
	Kind       string  `json:"kind" yaml:"kind"`
	Tools      []*Tool `json:"tools" yaml:"tools"`
	ImagesPath string  `json:"imagesPath" yaml:"imagesPath"`
	SlidesPath string  `json:"slidesPath" yaml:"slidesPath"`
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
		return fmt.Errorf("unexpected config kind: %s", c.APIVersion)
	}

	return nil
}

func (c *Config) GetTool(name string) *Tool {
	for _, tool := range c.Tools {
		if tool.Name == name {
			return tool
		}
	}

	return nil
}
