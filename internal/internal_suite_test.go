package internal_test

import (
	"testing"

	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"
	"github.com/petewall/eink-radiator/v2/internal"
)

func TestInternal(t *testing.T) {
	RegisterFailHandler(Fail)
	RunSpecs(t, "Internal Suite")
}

func MakeFakeSlide(name, slideType, duration string, params map[string]interface{}) *internal.Slide {
	if params == nil {
		params = map[string]interface{}{}
	}
	slide := &internal.Slide{
		Name:           name,
		Type:           slideType,
		DurationAmount: duration,
		Params:         params,
	}
	Expect(slide.Validate()).To(Succeed())
	return slide
}
