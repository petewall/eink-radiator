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
		log       *Buffer
		server    *internal.Server
		slideshow *internalfakes.FakeSlideshowAPI
	)

	BeforeEach(func() {
		log = NewBuffer()
		logObject := logrus.New()
		logObject.Out = log
		logObject.Level = logrus.DebugLevel
		slideshow = &internalfakes.FakeSlideshowAPI{}
		server = internal.NewServer(1234, slideshow, logObject)
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

})
