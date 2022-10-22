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
	ui        *UI
	log       *logrus.Logger
}

func NewServer(port int, slideshow SlideshowAPI, screen *Screen, ui *UI, log *logrus.Logger) *Server {
	server := &Server{
		port:      port,
		Router:    mux.NewRouter(),
		screen:    screen,
		slideshow: slideshow,
		ui:        ui,
		log:       log,
	}
	server.Router.HandleFunc("/", server.handleUI).Methods("GET")
	server.Router.PathPrefix("/static/").Handler(http.StripPrefix("/static/", http.FileServer(http.Dir("web/static/"))))

	server.Router.HandleFunc("/api/next", server.handleNext).Methods("POST")
	server.Router.HandleFunc("/api/prev", server.handlePrevious).Methods("POST")
	server.Router.HandleFunc("/api/screen/config.json", server.handleScreenConfig).Methods("GET")
	// server.Router.HandleFunc("/api/screen/image.png", server.handleScreenConfig).Methods("GET")

	server.Router.HandleFunc("/api/slides.json", server.handleSlides).Methods("GET")
	server.Router.HandleFunc("/api/slide/{name}/config.json", server.handleSlideConfig).Methods("GET")
	// server.Router.HandleFunc("/api/slide/{name}/image.png", server.handleSlideImage).Methods("GET")

	return server
}

func (s *Server) Start() error {
	s.log.Infof("Starting HTTP service on port %d", s.port)
	return http.ListenAndServe(fmt.Sprintf(":%d", s.port), s.Router)
}

func (s *Server) handleUI(w http.ResponseWriter, r *http.Request) {
	err := s.ui.Render(w, s.screen)
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

func (s *Server) handleSlides(w http.ResponseWriter, r *http.Request) {
	s.writeJSONResponse(w, s.slideshow.GetSlideConfig())
}

func (s *Server) handleSlideConfig(w http.ResponseWriter, r *http.Request) {
	name := mux.Vars(r)["name"]
	slide := s.slideshow.GetSlide(name)
	if slide == nil {
		w.WriteHeader(http.StatusNotFound)
		_, _ = fmt.Fprintf(w, "there are not any slides named \"%s\"", name)
		return
	}

	s.writeJSONResponse(w, slide)
}

// func (s *Server) handleSlideImage(w http.ResponseWriter, r *http.Request) {

// }
