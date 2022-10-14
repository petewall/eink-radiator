/*
Copyright © 2022 Pete Wall <pete@petewall.net>
*/
package cmd

import (
	"fmt"
	"os"
	"strings"

	"github.com/petewall/eink-radiator/v2/internal"
	"github.com/sirupsen/logrus"
	"github.com/spf13/cobra"
)

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

		logger.Info("Parsing slide config...")
		slideConfig, err := internal.ParseSlideConfigFromFile("configs/slides.yaml")
		if err != nil {
			return fmt.Errorf("failed to load slide config: %w", err)
		}
		logger.Infof("Finished parsing slide config: %d slides", len(slideConfig.Slides))

		logger.Info("Loading screen config...")
		screen, err := internal.LoadFromDriver("../eink-radiator-display/dist/main")
		if err != nil {
			return fmt.Errorf("failed to load screen config: %w", err)
		}
		logger.Infof("Finished loading screen config: %dx%d [%s]", screen.GetSize().Width, screen.GetSize().Height, strings.Join(screen.GetPalette(), ", "))

		slideshow := &internal.Slideshow{
			SlideConfig: slideConfig,
			Screen:      screen,
			ToolsPath:   "test/tools",
			ImagePath:   "test/images",
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
