package internal

import (
	"os"
)

type File interface {
	Name() string
	Write(b []byte) (n int, err error)
}

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

type FileRemover func(string) error

var RemoveFile FileRemover = os.Remove
