package internal

import (
	"os"
)

//go:generate go run github.com/maxbrunsfeld/counterfeiter/v6 . File
type File interface {
	Name() string
	Write(b []byte) (n int, err error)
}

//go:generate go run github.com/maxbrunsfeld/counterfeiter/v6 . TempFileMaker
type TempFileMaker func(pattern string, content []byte) (File, error)

var TempFile TempFileMaker = func(pattern string, content []byte) (File, error) {
	file, err := os.CreateTemp("", pattern)
	if err != nil {
		return nil, err
	}

	_, err = file.Write(content)
	if err != nil {
		return nil, err
	}

	return file, nil
}

//go:generate go run github.com/maxbrunsfeld/counterfeiter/v6 . FileRemover
type FileRemover func(string) error

var RemoveFile FileRemover = os.Remove
