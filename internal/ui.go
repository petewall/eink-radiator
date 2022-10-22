package internal

import (
	"fmt"
	"html/template"
	"io"
)

type UI struct {
	indexTemplate *template.Template
}

type TemplateData struct {
	Screen *Screen
}

func NewUI(path string) (*UI, error) {
	indexTemplate, err := template.ParseFiles(path)
	if err != nil {
		return nil, fmt.Errorf("failed to parse index.html template: %w", err)
	}
	return &UI{
		indexTemplate: indexTemplate,
	}, nil
}

func (ui *UI) Render(w io.Writer, screen *Screen) error {
	data := &TemplateData{
		Screen: screen,
	}
	return ui.indexTemplate.ExecuteTemplate(w, "index", data)
}
