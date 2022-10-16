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
						Name:     "TestSlide",
						Type:     "test",
						Duration: "30m",
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
					Name:     config.Slides[0].Name,
					Type:     "test",
					Duration: "30m",
				})
				err := config.Validate()
				Expect(err).To(HaveOccurred())
				Expect(err.Error()).To(Equal("slide #1 (TestSlide) has the same name as the earlier slide #0"))
			})
		})

		When("there is an invalid slides", func() {
			It("returns an error", func() {
				config.Slides[0].Duration = "what?"
				err := config.Validate()
				Expect(err).To(HaveOccurred())
				Expect(err.Error()).To(Equal("slide #0 (TestSlide) is not valid: slide duration is invalid: what?"))
			})
		})
	})
})

var _ = Describe("Slide", func() {
	var slide *internal.Slide
	BeforeEach(func() {
		slide = &internal.Slide{
			Name:     "TestSlide",
			Type:     "test",
			Duration: "30m",
		}
	})

	Describe("Validate", func() {
		It("validates the slide", func() {
			Expect(slide.Validate()).To(Succeed())
		})

		When("the name is empty", func() {
			It("returns an error", func() {
				slide.Name = ""
				err := slide.Validate()
				Expect(err).To(HaveOccurred())
				Expect(err.Error()).To(Equal("slide name cannot be empty"))
			})
		})

		When("the type is empty", func() {
			It("returns an error", func() {
				slide.Type = ""
				err := slide.Validate()
				Expect(err).To(HaveOccurred())
				Expect(err.Error()).To(Equal("slide type cannot be empty"))
			})
		})

		When("the duration is empty", func() {
			It("returns an error", func() {
				slide.Duration = ""
				err := slide.Validate()
				Expect(err).To(HaveOccurred())
				Expect(err.Error()).To(Equal("slide duration cannot be empty"))
			})
		})

		When("the duration is invalid", func() {
			It("returns an error", func() {
				slide.Duration = "not a valid duration"
				err := slide.Validate()
				Expect(err).To(HaveOccurred())
				Expect(err.Error()).To(Equal("slide duration is invalid: not a valid duration"))
			})
		})
	})

	Describe("GenerateImage", func() {
		XIt("calls the image source tool to generate an image", func() {
			By("creating a config file from the slide params", func() {})
			By("calling the image source tool", func() {})
		})

		When("creating the config file fails", func() {
			XIt("returns an error", func() {})
		})

		When("calling the image source tool fails", func() {
			XIt("returns an error", func() {})
		})
	})
})
