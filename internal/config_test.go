package internal_test

import (
	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"

	"github.com/petewall/eink-radiator/v2/internal"
	"github.com/petewall/eink-radiator/v2/pkg"
)

var _ = Describe("Config", func() {
	var config *internal.Config
	BeforeEach(func() {
		config = &internal.Config{
			APIVersion: internal.ConfigAPIVersion,
			Kind:       internal.ConfigKind,
			ImageSources: pkg.ImageSources{
				&pkg.ImageSource{
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
})
