package internal_test

import (
	"encoding/json"
	"errors"

	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"

	"github.com/petewall/eink-radiator/v2/internal"
	"github.com/petewall/eink-radiator/v2/internal/internalfakes"
)

var _ = Describe("Screen", func() {
	var (
		session        *internalfakes.FakeSession
		sessionFactory *internalfakes.FakeSessionFactory
	)

	BeforeEach(func() {
		session = &internalfakes.FakeSession{}
		sessionFactory = &internalfakes.FakeSessionFactory{}
		sessionFactory.Returns(session)

		internal.ExecCommand = sessionFactory.Spy
	})

	Describe("LoadFromDriver", func() {
		BeforeEach(func() {
			output := internal.ScreenDriver{
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
				screenPath, screenArgs := sessionFactory.ArgsForCall(0)
				Expect(screenPath).To(Equal("path/to/screen"))
				Expect(screenArgs).To(ConsistOf("config"))
			})

			By("returning a screen object", func() {
				size := screen.GetSize()
				Expect(size.Height).To(Equal(768))
				Expect(size.Width).To(Equal(1024))
				Expect(screen.GetPalette()).To(ConsistOf("red", "green", "blue"))
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
			screen := &internal.ScreenDriver{
				Path: "path/to/screen",
			}
			err := screen.SetImage("path/to/image.png")
			Expect(err).ToNot(HaveOccurred())

			By("calling the display command on the screen driver", func() {
				screenPath, screenArgs := sessionFactory.ArgsForCall(0)
				Expect(screenPath).To(Equal("path/to/screen"))
				Expect(screenArgs).To(ConsistOf("display", "path/to/image.png"))
			})
		})

		When("running the command fails", func() {
			BeforeEach(func() {
				session.RunReturns(errors.New("session failed"))
			})
			It("returns an error", func() {
				screen := &internal.ScreenDriver{
					Path: "path/to/screen",
				}
				err := screen.SetImage("path/to/image.png")
				Expect(err).To(HaveOccurred())
				Expect(err.Error()).To(Equal("failed to display the image path/to/image.png: session failed"))
			})
		})
	})
})
