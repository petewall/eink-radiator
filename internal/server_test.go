package internal_test

import (
	"net/http"
	"net/http/httptest"

	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"
	. "github.com/onsi/gomega/gbytes"
	"github.com/sirupsen/logrus"

	"github.com/petewall/eink-radiator/v2/internal"
	"github.com/petewall/eink-radiator/v2/internal/internalfakes"
)

var _ = Describe("Server", func() {
	var (
		config    *internal.Config
		log       *Buffer
		screen    *internal.Screen
		server    *internal.Server
		slideshow *internalfakes.FakeSlideshowAPI
	)

	BeforeEach(func() {
		config = &internal.Config{
			Port: 1234,
		}
		log = NewBuffer()
		logObject := logrus.New()
		logObject.Out = log
		logObject.Level = logrus.DebugLevel
		screen = &internal.Screen{
			Kind: "Test Screen",
			Size: &internal.ScreenSize{
				Width:  1024,
				Height: 768,
			},
			Palette: []string{"red", "green", "blue"},
		}
		slideshow = &internalfakes.FakeSlideshowAPI{}
		slideshow.GetSlideConfigReturns(&internal.SlideConfig{
			APIVersion: internal.SlideConfigAPIVersion,
			Kind:       internal.SlideConfigKind,
			Slides: []*internal.Slide{
				MakeFakeSlide("Slide1", "test", "1ms", nil),
				MakeFakeSlide("Slide2", "test", "1ms", nil),
				MakeFakeSlide("Slide3", "test", "1ms", nil),
			},
		})
		server = internal.NewServer(config, slideshow, screen, nil, logObject)
	})

	Describe("/api/next", func() {
		It("tells the slideshow to go to the next slide", func() {
			r := httptest.NewRequest(http.MethodPost, "/api/next", nil)
			w := httptest.NewRecorder()
			server.Router.ServeHTTP(w, r)

			Expect(slideshow.NextSlideCallCount()).To(Equal(1))
			Expect(w.Code).To(Equal(http.StatusOK))
			Expect(w.Body.String()).To(Equal("OK\n"))
		})
	})

	Describe("/api/prev", func() {
		It("tells the slideshow to go to the previous slide", func() {
			r := httptest.NewRequest(http.MethodPost, "/api/prev", nil)
			w := httptest.NewRecorder()
			server.Router.ServeHTTP(w, r)

			Expect(slideshow.PreviousSlideCallCount()).To(Equal(1))
			Expect(w.Code).To(Equal(http.StatusOK))
			Expect(w.Body.String()).To(Equal("OK\n"))
		})
	})

	Describe("/api/screen/config.json", func() {
		It("returns the screen configuration", func() {
			r := httptest.NewRequest(http.MethodGet, "/api/screen/config.json", nil)
			w := httptest.NewRecorder()
			server.Router.ServeHTTP(w, r)

			Expect(w.Code).To(Equal(http.StatusOK))
			Expect(w.Body.String()).To(MatchJSON(`{
				"kind": "Test Screen",
				"size": {
					"width": 1024,
					"height": 768
				},
				"palette": ["red", "green", "blue"]
			}`))
		})
	})

	Describe("/api/slides.json", func() {
		It("returns the list of slides", func() {
			r := httptest.NewRequest(http.MethodGet, "/api/slides.json", nil)
			w := httptest.NewRecorder()
			server.Router.ServeHTTP(w, r)

			Expect(w.Code).To(Equal(http.StatusOK))
			Expect(w.Body.String()).To(MatchJSON(`{
				"apiVersion": "v1.eink-radiator.petewall.net",
				"kind": "Slides",
				"slides": [
					{
						"name": "Slide1",
						"type": "test",
						"duration": "1ms",
						"params": {}
					},
					{
						"name": "Slide2",
						"type": "test",
						"duration": "1ms",
						"params": {}
					},
					{
						"name": "Slide3",
						"type": "test",
						"duration": "1ms",
						"params": {}
					}
				]
			}`))
		})
	})

	Describe("/api/slide/<name>/config.json", func() {
		BeforeEach(func() {
			slideshow.GetSlideReturns(MakeFakeSlide("Slide3", "test", "1ms", nil))
		})

		It("returns the of slide", func() {
			r := httptest.NewRequest(http.MethodGet, "/api/slide/Slide3/config.json", nil)
			w := httptest.NewRecorder()
			server.Router.ServeHTTP(w, r)

			Expect(w.Code).To(Equal(http.StatusOK))
			Expect(w.Body.String()).To(MatchJSON(`{
				"name": "Slide3",
				"type": "test",
				"duration": "1ms",
				"params": {}
			}`))
		})

		When("the slide is not found", func() {
			BeforeEach(func() {
				slideshow.GetSlideReturns(nil)
			})

			It("returns 404", func() {
				r := httptest.NewRequest(http.MethodGet, "/api/slide/WhatSlide/config.json", nil)
				w := httptest.NewRecorder()
				server.Router.ServeHTTP(w, r)

				Expect(w.Code).To(Equal(http.StatusNotFound))
				Expect(w.Body.String()).To(Equal("there are not any slides named \"WhatSlide\""))
			})
		})
	})
})
