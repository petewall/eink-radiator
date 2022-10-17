package internal

//go:generate go run github.com/maxbrunsfeld/counterfeiter/v6 -generate

//counterfeiter:generate . Logger
type Logger interface {
	Debug(args ...interface{})
	Infof(format string, args ...interface{})
}
