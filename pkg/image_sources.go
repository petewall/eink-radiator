package pkg

import (
	"fmt"
	"strconv"

	"gopkg.in/yaml.v3"

	"github.com/petewall/eink-radiator/v2/internal/helpers"
)

type ImageSources []*ImageSource

type ImageSource struct {
	Name string `json:"name" yaml:"name"`
	Path string `json:"path" yaml:"path"`
}

func (is ImageSources) List() []string {
	var sources []string
	for _, imageSource := range is {
		sources = append(sources, imageSource.Name)
	}
	return sources
}

func (is ImageSources) Get(name string) *ImageSource {
	for _, imageSource := range is {
		if imageSource.Name == name {
			return imageSource
		}
	}
	return nil
}

func (i *ImageSource) GenerateToBytes(name string, width, height int, config map[string]interface{}) ([]byte, error) {
	slideConfig, err := yaml.Marshal(config)
	if err != nil {
		return nil, fmt.Errorf("failed to prepare slide config: %w", err)
	}

	file, err := helpers.TempFile(name+"-"+i.Name+"-config-*.yaml", slideConfig)
	if err != nil {
		return nil, fmt.Errorf("failed to write slide config: %w", err)
	}

	// Need to do the anonymous function to appease the errcheck linter.
	// Since defer doesn't handle return values, and we need to explicitly
	// state that we're disregarding the error return value of RemoveFile
	defer func() { _ = helpers.RemoveFile(file.Name()) }()

	args := []string{
		"generate",
		"--config", file.Name(),
		"--width", strconv.Itoa(width),
		"--height", strconv.Itoa(height),
		"--to-stdout",
	}
	session := helpers.ExecCommand(i.Path, args...)
	err = session.Run()
	if err != nil {
		return nil, fmt.Errorf("image generator failed: %w", err)
	}

	output, err := session.Output()
	if err != nil {
		return nil, fmt.Errorf("failed to read image generator output: %w", err)
	}

	return output, nil
}

func (i *ImageSource) GenerateToFile(name, output string, width, height int, config map[string]interface{}) error {
	slideConfig, err := yaml.Marshal(config)
	if err != nil {
		return fmt.Errorf("failed to prepare slide config: %w", err)
	}

	file, err := helpers.TempFile(name+"-"+i.Name+"-config-*.yaml", slideConfig)
	if err != nil {
		return fmt.Errorf("failed to write slide config: %w", err)
	}

	// Need to do the anonymous function to appease the errcheck linter.
	// Since defer doesn't handle return values, and we need to explicitly
	// state that we're disregarding the error return value of RemoveFile
	defer func() { _ = helpers.RemoveFile(file.Name()) }()

	args := []string{
		"generate",
		"--config", file.Name(),
		"--width", strconv.Itoa(width),
		"--height", strconv.Itoa(height),
		"--output", output,
	}
	session := helpers.ExecCommand(i.Path, args...)
	err = session.Run()
	if err != nil {
		return fmt.Errorf("image generator failed: %w", err)
	}
	return nil
}
