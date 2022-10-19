package internal

import (
	"errors"
	"fmt"
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
