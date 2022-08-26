package internal

import (
	"fmt"
	"path"
	"time"

	"github.com/petewall/eink-radiator/v2/pkg"
	"github.com/spf13/viper"
)

type Rotation struct {
	ImageConfigs []pkg.ImageConfig
	index        int
}

func (r *Rotation) Start() {
	r.index = 0

	for {
		imageConfig := r.ImageConfigs[r.index]
		r.index = (r.index + 1) % len(r.ImageConfigs)

		imageGeneratorPath := path.Join(viper.GetString("imageSourcesPath"), imageConfig.Type)

		duration, err := time.ParseDuration(imageConfig.Duration)
		if err != nil {
			fmt.Printf("invalid duration: %s, skipping\n", imageConfig.Duration)

			continue
		}

		fmt.Printf("calling %s -s %s -c %s\n", imageGeneratorPath, viper.GetString("screen"), "???")
		time.Sleep(duration)
	}
}
