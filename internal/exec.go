package internal

import (
	"os/exec"
)

//go:generate go run github.com/maxbrunsfeld/counterfeiter/v6 . Session
type Session interface {
	Run() error
	Output() ([]byte, error)
}

//go:generate go run github.com/maxbrunsfeld/counterfeiter/v6 . SessionFactory
type SessionFactory func(name string, arg ...string) Session

var ExecCommand SessionFactory = func(name string, arg ...string) Session {
	return exec.Command(name, arg...)
}
