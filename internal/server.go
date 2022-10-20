package internal

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/sirupsen/logrus"
)

type Server struct {
	port int

	Router    *mux.Router
	screen    *Screen
	slideshow SlideshowAPI
	log       *logrus.Logger
}

func NewServer(port int, slideshow SlideshowAPI, screen *Screen, log *logrus.Logger) *Server {
	server := &Server{
		port:      port,
		Router:    mux.NewRouter(),
		screen:    screen,
		slideshow: slideshow,
		log:       log,
	}
	server.Router.HandleFunc("/api/next", server.handleNext).Methods("POST")
	server.Router.HandleFunc("/api/prev", server.handlePrevious).Methods("POST")
	server.Router.HandleFunc("/api/screen/config.json", server.handleScreenConfig).Methods("GET")
	return server
}

func (s *Server) Start() error {
	s.log.Infof("Starting HTTP service on port %d", s.port)
	return http.ListenAndServe(fmt.Sprintf(":%d", s.port), s.Router)
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

func (s *Server) handleScreenConfig(w http.ResponseWriter, r *http.Request) {
	screenConfig, err := json.Marshal(s.screen)
	if err != nil {
		s.log.WithError(err).Warn("failed to prepare screen config")
		w.WriteHeader(http.StatusInternalServerError)
		_, _ = fmt.Fprintln(w, "failed to prepare screen config")
	}
	w.Header().Set("Content-type", "application/json")
	w.WriteHeader(http.StatusOK)
	_, _ = w.Write(screenConfig)
}
