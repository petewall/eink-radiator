package internal_test

import (
	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"

	"github.com/petewall/eink-radiator/v2/internal"
)

var _ = Describe("SlideConfig", func() {
	Describe("Validate", func() {
		var config *internal.SlideConfig
		BeforeEach(func() {
			config = &internal.SlideConfig{
				APIVersion: internal.SlideConfigAPIVersion,
				Kind:       internal.SlideConfigKind,
				Slides: []*internal.Slide{
					&internal.Slide{
						Name:           "TestSlide",
						Type:           "test",
						DurationAmount: "30m",
					},
				},
			}
		})
		It("validates the slide config", func() {
			Expect(config.Validate()).To(Succeed())
		})

		When("the api version is wrong", func() {
			It("returns an error", func() {
				config.APIVersion = "what.is.this"
				err := config.Validate()
				Expect(err).To(HaveOccurred())
				Expect(err.Error()).To(Equal("unexpected slide config API version: what.is.this"))
			})
		})

		When("the kind is wrong", func() {
			It("returns an error", func() {
				config.Kind = "WhatIsThis"
				err := config.Validate()
				Expect(err).To(HaveOccurred())
				Expect(err.Error()).To(Equal("unexpected slide config kind: WhatIsThis"))
			})
		})

		When("there are no slides", func() {
			It("returns an error", func() {
				config.Slides = []*internal.Slide{}
				err := config.Validate()
				Expect(err).To(HaveOccurred())
				Expect(err.Error()).To(Equal("slide config does not contain any slides"))
			})
		})

		When("there are multiple slides with the same name", func() {
			It("returns an error", func() {
				config.Slides = append(config.Slides, &internal.Slide{
					Name:           config.Slides[0].Name,
					Type:           "test",
					DurationAmount: "30m",
				})
				err := config.Validate()
				Expect(err).To(HaveOccurred())
				Expect(err.Error()).To(Equal("slide #1 (TestSlide) has the same name as the earlier slide #0"))
			})
		})

		When("there is an invalid slides", func() {
			It("returns an error", func() {
				config.Slides[0].DurationAmount = "what?"
				err := config.Validate()
				Expect(err).To(HaveOccurred())
				Expect(err.Error()).To(Equal("slide #0 (TestSlide) is not valid: slide duration is invalid: what?"))
			})
		})
	})
})
