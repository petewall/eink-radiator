package internal_test

import (
	"encoding/json"
	"errors"
	"strings"

	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"

	"github.com/petewall/eink-radiator/v2/internal"
	"github.com/petewall/eink-radiator/v2/internal/helpers"
	"github.com/petewall/eink-radiator/v2/internal/helpers/helpersfakes"
)

var _ = Describe("Screen", func() {
	var (
		config         *internal.Config
		session        *helpersfakes.FakeSession
		sessionFactory *helpersfakes.FakeSessionFactory
	)

	BeforeEach(func() {
		config = &internal.Config{
			ImagesPath: "/path/to/images",
		}
		session = &helpersfakes.FakeSession{}
		sessionFactory = &helpersfakes.FakeSessionFactory{}
		sessionFactory.Returns(session)

		helpers.ExecCommand = sessionFactory.Spy
	})

	Describe("LoadFromDriver", func() {
		BeforeEach(func() {
			output := internal.Screen{
				Size: &internal.ScreenSize{
					Height: 768,
					Width:  1024,
				},
				Palette: []string{"red", "green", "blue"},
			}
			outputBytes, err := json.Marshal(output)
			Expect(err).ToNot(HaveOccurred())
			session.OutputReturns(outputBytes, nil)
		})
		It("loads a screen config from the output of the screen driver", func() {
			screen, err := internal.LoadFromDriver("path/to/screen")
			Expect(err).ToNot(HaveOccurred())

			By("calling the config command on the screen driver", func() {
				Expect(sessionFactory.CallCount()).To(Equal(1))
				screenPath, screenArgs := sessionFactory.ArgsForCall(0)
				Expect(screenPath).To(Equal("path/to/screen"))
				Expect(screenArgs).To(ConsistOf("config"))
			})

			By("returning a screen object", func() {
				Expect(screen.Size.Height).To(Equal(768))
				Expect(screen.Size.Width).To(Equal(1024))
				Expect(screen.Palette).To(ConsistOf("red", "green", "blue"))
			})
		})

		When("running the command fails", func() {
			BeforeEach(func() {
				session.OutputReturns(nil, errors.New("session failed"))
			})
			It("returns an error", func() {
				_, err := internal.LoadFromDriver("path/to/screen")
				Expect(err).To(HaveOccurred())
				Expect(err.Error()).To(Equal("failed to get screen config from path/to/screen: session failed"))
			})
		})

		When("the screen driver returns an invalid config", func() {
			BeforeEach(func() {
				session.OutputReturns([]byte("this - is ~ not & json"), nil)
			})
			It("returns an error", func() {
				_, err := internal.LoadFromDriver("path/to/screen")
				Expect(err).To(HaveOccurred())
				Expect(err.Error()).To(Equal("failed to parse screen config from path/to/screen: invalid character 'h' in literal true (expecting 'r')"))
			})
		})
	})

	Describe("SetImage", func() {
		It("calls the display driver with an image", func() {
			screen := &internal.Screen{
				Path: "path/to/screen",
			}
			err := screen.SetImage(config, "path/to/image.png")
			Expect(err).ToNot(HaveOccurred())

			By("calling the display command on the screen driver", func() {
				screenPath, screenArgs := sessionFactory.ArgsForCall(0)
				Expect(screenPath).To(Equal("path/to/screen"))
				Expect(screenArgs).To(ConsistOf(strings.Split("display path/to/image.png --save /path/to/images/screen.png", " ")))
			})
		})

		When("running the command fails", func() {
			BeforeEach(func() {
				session.RunReturns(errors.New("session failed"))
			})
			It("returns an error", func() {
				screen := &internal.Screen{
					Path: "path/to/screen",
				}
				err := screen.SetImage(config, "path/to/image.png")
				Expect(err).To(HaveOccurred())
				Expect(err.Error()).To(Equal("failed to display the image path/to/image.png: session failed"))
			})
		})
	})
})
