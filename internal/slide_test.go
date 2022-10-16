package internal_test

import (
	"errors"

	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"

	"github.com/petewall/eink-radiator/v2/internal"
	"github.com/petewall/eink-radiator/v2/internal/internalfakes"
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
			Params: map[string]interface{}{
				"location": "earth",
				"glorious": true,
			},
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
		var (
			tool           *internal.Tool
			screen         *internal.ScreenSize
			file           *internalfakes.FakeFile
			tempFile       *internalfakes.FakeTempFileMaker
			removeFile     *internalfakes.FakeFileRemover
			session        *internalfakes.FakeSession
			sessionFactory *internalfakes.FakeSessionFactory
		)

		BeforeEach(func() {
			tool = &internal.Tool{
				Name: "test",
				Path: "/path/to/test",
			}
			screen = &internal.ScreenSize{
				Width:  1024,
				Height: 768,
			}

			file = &internalfakes.FakeFile{}
			file.NameReturns("/tmp/TestSlide-test-config-1234.yaml")
			tempFile = &internalfakes.FakeTempFileMaker{}
			tempFile.Returns(file, nil)
			removeFile = &internalfakes.FakeFileRemover{}
			internal.TempFile = tempFile.Spy
			internal.RemoveFile = removeFile.Spy

			session = &internalfakes.FakeSession{}
			sessionFactory = &internalfakes.FakeSessionFactory{}
			sessionFactory.Returns(session)

			internal.ExecCommand = sessionFactory.Spy
		})

		It("calls the image source tool to generate an image", func() {
			imagePath, err := slide.GenerateImage(tool, "/path/to/images", screen)
			Expect(err).ToNot(HaveOccurred())

			By("creating a config file from the slide params", func() {
				Expect(tempFile.CallCount()).To(Equal(1))
				name, content := tempFile.ArgsForCall(0)
				Expect(name).To(Equal("TestSlide-test-config-*.yaml"))
				Expect(content).To(MatchYAML("location: earth\nglorious: true"))
				Expect(tempFile.CallCount()).To(Equal(1))

				Expect(removeFile.CallCount()).To(Equal(1))
				Expect(removeFile.ArgsForCall(0)).To(Equal("/tmp/TestSlide-test-config-1234.yaml"))
			})

			By("calling the image source tool", func() {
				Expect(sessionFactory.CallCount()).To(Equal(1))
				screenPath, screenArgs := sessionFactory.ArgsForCall(0)
				Expect(screenPath).To(Equal("/path/to/test"))
				Expect(screenArgs).To(ConsistOf("generate",
					"--config", "/tmp/TestSlide-test-config-1234.yaml",
					"--height", "768",
					"--width", "1024",
					"--output", "/path/to/images/TestSlide.png",
				))
			})

			By("returning the image path", func() {
				Expect(imagePath).To(Equal("/path/to/images/TestSlide.png"))
			})
		})

		When("creating the config file fails", func() {
			BeforeEach(func() {
				tempFile.Returns(nil, errors.New("temp file failed"))
			})

			It("returns an error", func() {
				_, err := slide.GenerateImage(tool, "/path/to/images", screen)
				Expect(err).To(HaveOccurred())
				Expect(err.Error()).To(Equal("failed to write slide config: temp file failed"))
			})
		})

		When("calling the image source tool fails", func() {
			BeforeEach(func() {
				session.RunReturns(errors.New("session run failed"))
			})

			It("returns an error", func() {
				_, err := slide.GenerateImage(tool, "/path/to/images", screen)
				Expect(err).To(HaveOccurred())
				Expect(err.Error()).To(Equal("image generator failed: session run failed"))
			})
		})
	})
})
