package internal_test

import (
	"strings"
	"time"

	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"
	. "github.com/onsi/gomega/gbytes"
	"github.com/sirupsen/logrus"

	"github.com/petewall/eink-radiator/v2/internal"
	"github.com/petewall/eink-radiator/v2/internal/internalfakes"
)

var _ = Describe("Slideshow", func() {
	var (
		config    *internal.Config
		slides    *internal.SlideConfig
		screen    *internal.Screen
		log       *logrus.Logger
		logBuffer *Buffer

		tempFile       *internalfakes.FakeTempFileMaker
		removeFile     *internalfakes.FakeFileRemover
		session        *internalfakes.FakeSession
		sessionFactory *internalfakes.FakeSessionFactory
	)

	BeforeEach(func() {
		tool := &internal.Tool{
			Name: "test",
			Path: "/path/to/test",
		}
		config = &internal.Config{
			Tools:      []*internal.Tool{tool},
			ImagesPath: "/path/to/images",
		}

		slides = &internal.SlideConfig{
			APIVersion: internal.SlideConfigAPIVersion,
			Kind:       internal.SlideConfigKind,
			Slides: []*internal.Slide{
				&internal.Slide{
					Name:     "Slide1",
					Type:     "test",
					Duration: time.Millisecond,
					Params:   map[string]interface{}{},
				},
				&internal.Slide{
					Name:     "Slide2",
					Type:     "test",
					Duration: time.Millisecond,
					Params:   map[string]interface{}{},
				},
				&internal.Slide{
					Name:     "Slide3",
					Type:     "test",
					Duration: time.Millisecond,
					Params:   map[string]interface{}{},
				},
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

		file := &internalfakes.FakeFile{}
		file.NameReturnsOnCall(0, "/tmp/Slide1-test-config-1111.yaml")
		file.NameReturnsOnCall(1, "/tmp/Slide2-test-config-2222.yaml")
		file.NameReturnsOnCall(2, "/tmp/Slide3-test-config-3333.yaml")
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
				Expect(args).To(ConsistOf(strings.Split("display /path/to/images/Slide1.png", " ")))
			})

			By("stopping", func() {
				Expect(logBuffer).Should(Say(`level=debug msg="action requested: stop"`))
			})
		})
	})
})
