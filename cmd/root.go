/*
Copyright © 2022 Pete Wall <pete@petewall.net>
*/
package cmd

import (
	"fmt"
	"os"
	"strings"

	"github.com/sirupsen/logrus"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
	"gopkg.in/yaml.v3"

	"github.com/petewall/eink-radiator/v2/internal"
)

func ParseConfigFromFile(path string, dest interface{}) error {
	contents, err := os.ReadFile(path)
	if err != nil {
		return fmt.Errorf("failed to read config file %s: %w", path, err)
	}

	err = yaml.Unmarshal(contents, dest)
	if err != nil {
		return fmt.Errorf("failed to parse config file %s: %w", path, err)
	}
	return nil
}

var rootCmd = &cobra.Command{
	Use:   "eink-radiator",
	Short: "Main process for the eInk Radiator",
	RunE: func(cmd *cobra.Command, args []string) error {
		logger := logrus.New()
		logger.Out = cmd.ErrOrStderr()
		logger.Level = logrus.DebugLevel

		config := &internal.Config{}
		err := ParseConfigFromFile(viper.GetString("config"), config)
		if err != nil {
			return fmt.Errorf("failed to load config: %w", err)
		}
		err = config.Validate()
		if err != nil {
			return fmt.Errorf("config is not valid: %w", err)
		}
		logger.Infof("Parsed config (%s)", viper.GetString("config"))

		slideConfig := &internal.SlideConfig{}
		err = ParseConfigFromFile(config.SlidesPath, slideConfig)
		if err != nil {
			return fmt.Errorf("failed to load slide config: %w", err)
		}
		err = slideConfig.Validate()
		if err != nil {
			return fmt.Errorf("slide config is not valid: %w", err)
		}
		logger.Infof("Parsed slide config (%s): %d slides", config.SlidesPath, len(slideConfig.Slides))

		screen, err := internal.LoadFromDriver(config.ScreenPath)
		if err != nil {
			return fmt.Errorf("failed to load screen config: %w", err)
		}
		logger.Infof("Loaded screen config: %dx%d [%s]", screen.Size.Width, screen.Size.Height, strings.Join(screen.Palette, ", "))

		ui, err := internal.NewUI("web/templates/index.html")
		if err != nil {
			return fmt.Errorf("failed to create UI: %w", err)
		}
		logger.Info("User interface module loaded")

		slideshow := internal.NewSlideshow(config, slideConfig, screen, logger)
		server := internal.NewServer(config, slideshow, screen, ui, logger)

		go slideshow.Start()
		return server.Start()
	},
}

func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {
	// rootCmd.Flags().Int("port", 8000, "the port number for the HTTP service to listen on")
	rootCmd.Flags().StringP("config", "c", "config.yaml", "the config file")
	_ = viper.BindPFlags(rootCmd.Flags())
}
