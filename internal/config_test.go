package internal_test

import (
	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"

	"github.com/petewall/eink-radiator/v2/internal"
)

var _ = Describe("Config", func() {
	var config *internal.Config
	BeforeEach(func() {
		config = &internal.Config{
			APIVersion: internal.ConfigAPIVersion,
			Kind:       internal.ConfigKind,
			Tools: []*internal.Tool{
				&internal.Tool{
					Name: "test",
					Path: "/path/to/test",
				},
			},
			ImagesPath: "/path/to/images",
			SlidesPath: "/path/to/slides",
		}
	})

	Describe("Validate", func() {
		It("validates the config", func() {
			Expect(config.Validate()).To(Succeed())
		})

		When("the api version is wrong", func() {
			It("returns an error", func() {
				config.APIVersion = "what.is.this"
				err := config.Validate()
				Expect(err).To(HaveOccurred())
				Expect(err.Error()).To(Equal("unexpected config API version: what.is.this"))
			})
		})

		When("the kind is wrong", func() {
			It("returns an error", func() {
				config.Kind = "WhatIsThis"
				err := config.Validate()
				Expect(err).To(HaveOccurred())
				Expect(err.Error()).To(Equal("unexpected config kind: WhatIsThis"))
			})
		})
	})

	Describe("GetTool", func() {
		It("returns the tool based on the name", func() {
			tool := config.GetTool("test")
			Expect(tool).ToNot(BeNil())
			Expect(tool.Name).To(Equal("test"))
			Expect(tool.Path).To(Equal("/path/to/test"))
		})

		When("the tool doesn't exist", func() {
			It("returns nil", func() {
				tool := config.GetTool("magic")
				Expect(tool).To(BeNil())
			})
		})
	})
})
