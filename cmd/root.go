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

// func RunSerially(funcs ...func(cmd *cobra.Command, args []string) error) func(cmd *cobra.Command, args []string) error {
// 	return func(cmd *cobra.Command, args []string) error {
// 		for _, fn := range funcs {
// 			err := fn(cmd, args)
// 			if err != nil {
// 				return err
// 			}
// 		}

// 		return nil
// 	}
// }

var rootCmd = &cobra.Command{
	Use:   "eink-radiator",
	Short: "Main process for the eInk Radiator",
	RunE: func(cmd *cobra.Command, args []string) error {
		logger := logrus.New()
		logger.Out = cmd.ErrOrStderr()
		logger.Level = logrus.DebugLevel

		configPath := "test/config.yaml"
		logger.Infof("Parsing config (%s)...", configPath)
		config := &internal.Config{}
		err := ParseConfigFromFile(configPath, config)
		if err != nil {
			return fmt.Errorf("failed to load config: %w", err)
		}
		err = config.Validate()
		if err != nil {
			return fmt.Errorf("config is not valid: %w", err)
		}
		logger.Info("Finished parsing config")

		logger.Infof("Parsing slide config (%s)...", config.SlidesPath)
		slideConfig := &internal.SlideConfig{}
		err = ParseConfigFromFile(config.SlidesPath, slideConfig)
		if err != nil {
			return fmt.Errorf("failed to load slide config: %w", err)
		}
		err = slideConfig.Validate()
		if err != nil {
			return fmt.Errorf("slide config is not valid: %w", err)
		}
		logger.Infof("Finished parsing slide config: %d slides", len(slideConfig.Slides))

		logger.Info("Loading screen config...")
		screen, err := internal.LoadFromDriver(config.GetTool("screen").Path)
		if err != nil {
			return fmt.Errorf("failed to load screen config: %w", err)
		}
		logger.Infof("Finished loading screen config: %dx%d [%s]", screen.GetSize().Width, screen.GetSize().Height, strings.Join(screen.GetPalette(), ", "))

		slideshow := &internal.Slideshow{
			Config:      config,
			SlideConfig: slideConfig,
			Screen:      screen,
			Logger:      logger,
		}
		slideshow.Start()

		return nil
	},
}

func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {
}
