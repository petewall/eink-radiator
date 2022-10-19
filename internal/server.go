package internal

import (
	"fmt"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/sirupsen/logrus"
)

type Server struct {
	port int

	Router    *mux.Router
	slideshow SlideshowAPI
	log       *logrus.Logger
}

func NewServer(port int, slideshow SlideshowAPI, log *logrus.Logger) *Server {
	server := &Server{
		port:      port,
		Router:    mux.NewRouter(),
		slideshow: slideshow,
		log:       log,
	}
	server.Router.HandleFunc("/api/next", server.handleNext).Methods("POST")
	server.Router.HandleFunc("/api/prev", server.handlePrevious).Methods("POST")
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
