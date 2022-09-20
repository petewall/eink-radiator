package internal

import (
	"fmt"
	"path"
	"time"

	"github.com/petewall/eink-radiator/v2/pkg"
	"github.com/sirupsen/logrus"
	"github.com/spf13/viper"
)

type Rotation struct {
	ImageConfigs []pkg.ImageConfig
	index        int
	Logger       *logrus.Logger
}

func (r *Rotation) Start() {
	r.index = 0

	for {
		imageConfig := r.ImageConfigs[r.index]
		r.index = (r.index + 1) % len(r.ImageConfigs)

		imageGeneratorPath := path.Join(viper.GetString("imageSourcesPath"), imageConfig.Type)

		duration, err := time.ParseDuration(imageConfig.Duration)
		if err != nil {
			r.Logger.Warn(fmt.Sprintf("invalid duration %s, skipping", imageConfig.Duration))

			continue
		}

		r.Logger.Debug(fmt.Sprintf("calling %s -s %s -c %s", imageGeneratorPath, viper.GetString("screen"), "???"))
		time.Sleep(duration)
	}
}
