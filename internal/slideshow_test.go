package internal_test

import (
	"strings"

	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"
	. "github.com/onsi/gomega/gbytes"
	"github.com/sirupsen/logrus"

	"github.com/petewall/eink-radiator/v2/internal"
	"github.com/petewall/eink-radiator/v2/internal/helpers"
	"github.com/petewall/eink-radiator/v2/internal/helpers/helpersfakes"
	"github.com/petewall/eink-radiator/v2/pkg"
)

var _ = Describe("Slideshow", func() {
	var (
		config    *internal.Config
		slides    *internal.SlideConfig
		screen    *internal.Screen
		log       *logrus.Logger
		logBuffer *Buffer

		tempFile       *helpersfakes.FakeTempFileMaker
		removeFile     *helpersfakes.FakeFileRemover
		session        *helpersfakes.FakeSession
		sessionFactory *helpersfakes.FakeSessionFactory
	)

	BeforeEach(func() {
		imageSource := &pkg.ImageSource{
			Name: "test",
			Path: "/path/to/test",
		}
		config = &internal.Config{
			ImageSources: pkg.ImageSources{imageSource},
			ImagesPath:   "/path/to/images",
		}

		slides = &internal.SlideConfig{
			APIVersion: internal.SlideConfigAPIVersion,
			Kind:       internal.SlideConfigKind,
			Slides: []*internal.Slide{
				MakeFakeSlide("Slide1", "test", "1ms", nil),
				MakeFakeSlide("Slide2", "test", "1ms", nil),
				MakeFakeSlide("Slide3", "test", "1ms", nil),
			},
		}

		screen = &internal.Screen{
			Path: "/path/to/screen",
			Size: &internal.ScreenSize{
				Width:  640,
				Height: 480,
			},
		}

		logBuffer = NewBuffer()
		log = logrus.New()
		log.Out = logBuffer
		log.Level = logrus.DebugLevel

		file := &helpersfakes.FakeFile{}
		file.NameReturnsOnCall(0, "/tmp/Slide1-test-config-1111.yaml")
		file.NameReturnsOnCall(1, "/tmp/Slide2-test-config-2222.yaml")
		file.NameReturnsOnCall(2, "/tmp/Slide3-test-config-3333.yaml")
		tempFile = &helpersfakes.FakeTempFileMaker{}
		tempFile.Returns(file, nil)
		removeFile = &helpersfakes.FakeFileRemover{}
		helpers.TempFile = tempFile.Spy
		helpers.RemoveFile = removeFile.Spy

		session = &helpersfakes.FakeSession{}
		sessionFactory = &helpersfakes.FakeSessionFactory{}
		sessionFactory.Returns(session)

		helpers.ExecCommand = sessionFactory.Spy
	})

	Describe("GetSlide", func() {
		It("returns the slide with the matching name", func() {
			slideshow := internal.NewSlideshow(config, slides, screen, log)
			slide := slideshow.GetSlide("Slide2")
			Expect(slide.Name).To(Equal("Slide2"))
			Expect(slide.Type).To(Equal("test"))
			Expect(slide.DurationAmount).To(Equal("1ms"))
		})

		When("the slide is not found", func() {
			It("returns nil", func() {
				slideshow := internal.NewSlideshow(config, slides, screen, log)
				slide := slideshow.GetSlide("UnknownSlide")
				Expect(slide).To(BeNil())
			})
		})
	})

	Describe("GetSlideConfig", func() {
		It("returns the slide config", func() {
			slideshow := internal.NewSlideshow(config, slides, screen, log)
			slideConfig := slideshow.GetSlideConfig()
			Expect(slideConfig).To(Equal(slides))
		})
	})

	Describe("Start", func() {
		It("starts the slideshow", func() {
			slideshow := internal.NewSlideshow(config, slides, screen, log)
			slideshow.Stop() // Pre-populate the action channel with a stop request
			slideshow.Start()

			By("starting at 0", func() {
				Expect(logBuffer).Should(Say(`level=debug msg="generating image for slide 0 \(Slide1\)..."`))
			})
			By("generating the image", func() {
				cli, args := sessionFactory.ArgsForCall(0)
				Expect(cli).To(Equal("/path/to/test"))
				Expect(args).To(ConsistOf(strings.Split("generate --config /tmp/Slide1-test-config-1111.yaml --height 480 --width 640 --output /path/to/images/Slide1.png", " ")))
			})

			By("displaying the image", func() {
				cli, args := sessionFactory.ArgsForCall(1)
				Expect(cli).To(Equal("/path/to/screen"))
				Expect(args).To(ConsistOf(strings.Split("display /path/to/images/Slide1.png --save /path/to/images/screen.png", " ")))
			})

			By("stopping", func() {
				Expect(logBuffer).Should(Say(`level=debug msg="action requested: stop"`))
			})
		})
	})
})
