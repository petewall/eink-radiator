package internal

import (
	"os/exec"
)

//go:generate go run github.com/maxbrunsfeld/counterfeiter/v6 -generate

//counterfeiter:generate . Session
type Session interface {
	Run() error
	Output() ([]byte, error)
}

//counterfeiter:generate . SessionFactory
type SessionFactory func(name string, arg ...string) Session

var ExecCommand SessionFactory = func(name string, arg ...string) Session {
	return exec.Command(name, arg...)
}
