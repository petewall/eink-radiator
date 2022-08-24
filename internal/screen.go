package internal

import (
	"github.com/petewall/eink-radiator/v2/pkg"
)

type Screen struct {
	Config pkg.ScreenConfig
}

func (s *Screen) SetImage(path string) error {
	return nil
}
