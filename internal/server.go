package internal

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"path/filepath"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/sirupsen/logrus"
)

type Server struct {
	Router    *chi.Mux
	config    *Config
	screen    *Screen
	slideshow SlideshowAPI
	ui        *UI
	log       *logrus.Logger
}

func NewServer(config *Config, slideshow SlideshowAPI, screen *Screen, ui *UI, log *logrus.Logger) *Server {
	server := &Server{
		Router:    chi.NewRouter(),
		config:    config,
		screen:    screen,
		slideshow: slideshow,
		ui:        ui,
		log:       log,
	}

	server.Router.Use(middleware.RequestLogger(&middleware.DefaultLogFormatter{Logger: log, NoColor: false}))

	server.Router.Get("/", server.handleUI)
	server.Router.Handle("/static/*", http.StripPrefix("/static", http.FileServer(http.Dir("web/static"))))

	server.Router.Post("/api/next", server.handleNext)
	server.Router.Post("/api/prev", server.handlePrevious)
	server.Router.Get("/api/screen/config.json", server.handleScreenConfig)

	server.Router.Get("/api/slides.json", server.handleSlides)
	server.Router.Get("/api/slide/{name}/config.json", server.handleSlideConfig)

	server.Router.Group(func(r chi.Router) {
		r.Use(middleware.NoCache)
		r.Get("/api/screen/image.png", server.handleScreenImage)
		r.Get("/api/slide/{name}/image.png", server.handleSlideImage)
	})

	return server
}

func (s *Server) Start() error {
	s.log.Infof("Starting HTTP service on port %d", s.config.Port)
	return http.ListenAndServe(fmt.Sprintf(":%d", s.config.Port), s.Router)
}

func (s *Server) handleUI(w http.ResponseWriter, r *http.Request) {
	err := s.ui.Render(w, s.screen, s.slideshow.GetSlides())
	if err != nil {
		s.log.WithError(err).Warn("failed to render ui template")
		w.WriteHeader(http.StatusInternalServerError)
		_, _ = fmt.Fprintln(w, "failed to render ui template")
		return
	}
}

func (s *Server) handleNext(w http.ResponseWriter, r *http.Request) {
	s.slideshow.NextSlide()
	w.WriteHeader(http.StatusOK)
	_, _ = fmt.Fprintln(w, http.StatusText(http.StatusOK))
}

func (s *Server) handlePrevious(w http.ResponseWriter, r *http.Request) {
	s.slideshow.PreviousSlide()
	w.WriteHeader(http.StatusOK)
	_, _ = fmt.Fprintln(w, http.StatusText(http.StatusOK))
}

func (s *Server) writeJSONResponse(w http.ResponseWriter, object interface{}) {
	bytes, err := json.Marshal(object)
	if err != nil {
		s.log.WithError(err).Warn("failed to prepare response")
		w.WriteHeader(http.StatusInternalServerError)
		_, _ = fmt.Fprintln(w, "failed to prepare response")
		return
	}
	w.Header().Set("Content-type", "application/json")
	w.WriteHeader(http.StatusOK)
	_, _ = w.Write(bytes)
}

func (s *Server) handleScreenConfig(w http.ResponseWriter, r *http.Request) {
	s.writeJSONResponse(w, s.screen)
}

func (s *Server) handleScreenImage(w http.ResponseWriter, r *http.Request) {
	screenImageFile := filepath.Join(s.config.ImagesPath, "screen.png")
	buf, err := os.ReadFile(screenImageFile)
	if err != nil {
		s.log.WithError(err).Warn("failed to read screen image")
		w.WriteHeader(http.StatusInternalServerError)
		_, _ = fmt.Fprintln(w, "failed to read screen image")
		return
	}

	w.Header().Set("Content-Type", "image/png")
	_, _ = w.Write(buf)
}

func (s *Server) handleSlides(w http.ResponseWriter, r *http.Request) {
	s.writeJSONResponse(w, s.slideshow.GetSlideConfig())
}

func (s *Server) handleSlideConfig(w http.ResponseWriter, r *http.Request) {
	name := chi.URLParam(r, "name")
	slide := s.slideshow.GetSlide(name)
	if slide == nil {
		w.WriteHeader(http.StatusNotFound)
		_, _ = fmt.Fprintf(w, "there are not any slides named \"%s\"", name)
		return
	}

	s.writeJSONResponse(w, slide)
}

func (s *Server) handleSlideImage(w http.ResponseWriter, r *http.Request) {
	name := chi.URLParam(r, "name")
	slide := s.slideshow.GetSlide(name)
	if slide == nil {
		w.WriteHeader(http.StatusNotFound)
		_, _ = fmt.Fprintf(w, "there are not any slides named \"%s\"", name)
		return
	}

	imageFile, err := slide.GetImage(s.config, s.screen.Size)
	if err != nil {
		s.log.WithError(err).Warnf("failed to get image for slide \"%s\"", name)
		w.WriteHeader(http.StatusInternalServerError)
		_, _ = fmt.Fprintf(w, "failed to get image for slide \"%s\"\n", name)
		return
	}

	buf, err := os.ReadFile(imageFile)
	if err != nil {
		s.log.WithError(err).Warnf("failed to read image for slide \"%s\"", name)
		w.WriteHeader(http.StatusInternalServerError)
		_, _ = fmt.Fprintf(w, "failed to read image for slide \"%s\"\n", name)
		return
	}

	w.Header().Set("Content-Type", "image/png")
	_, _ = w.Write(buf)
}
