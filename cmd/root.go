/*
Copyright © 2022 Pete Wall <pete@petewall.net>
*/
package cmd

import (
	"fmt"
	"os"
	"strings"

	"gopkg.in/yaml.v3"

	"github.com/petewall/eink-radiator/v2/internal"
	"github.com/sirupsen/logrus"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
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

		configPath := "test/config.yaml"
		config := &internal.Config{}
		err := ParseConfigFromFile(configPath, config)
		if err != nil {
			return fmt.Errorf("failed to load config: %w", err)
		}
		err = config.Validate()
		if err != nil {
			return fmt.Errorf("config is not valid: %w", err)
		}
		logger.Infof("Parsed config (%s)", configPath)

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

		screen, err := internal.LoadFromDriver(config.GetTool("screen").Path)
		if err != nil {
			return fmt.Errorf("failed to load screen config: %w", err)
		}
		logger.Infof("Loaded screen config: %dx%d [%s]", screen.GetSize().Width, screen.GetSize().Height, strings.Join(screen.GetPalette(), ", "))

		slideshow := &internal.Slideshow{
			Config:      config,
			SlideConfig: slideConfig,
			Screen:      screen,
			Logger:      logger,
		}

		server := internal.NewServer(viper.GetInt("port"), slideshow, logger)

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
	rootCmd.Flags().Int("port", 8000, "the port number for the HTTP service to listen on")
	_ = viper.BindPFlags(rootCmd.Flags())
}
