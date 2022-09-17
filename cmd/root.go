/*
Copyright © 2022 Pete Wall <pete@petewall.net>
*/
package cmd

import (
	"errors"
	"fmt"
	"os"

	"github.com/ghodss/yaml"
	"github.com/petewall/eink-radiator/v2/internal"
	"github.com/petewall/eink-radiator/v2/pkg"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

func RunSerially(funcs ...func(cmd *cobra.Command, args []string) error) func(cmd *cobra.Command, args []string) error {
	return func(cmd *cobra.Command, args []string) error {
		for _, fn := range funcs {
			err := fn(cmd, args)
			if err != nil {
				return err
			}
		}

		return nil
	}
}

var ErrMissingSreenConfig = errors.New("missing data file path. Please run again with --data defined")

func ParseScreenConfig(cmd *cobra.Command, args []string) error {
	configFilePath := viper.GetString("screen")
	if configFilePath == "" {
		return ErrMissingSreenConfig
	}

	configFileData, err := os.ReadFile(configFilePath)
	if err != nil {
		return fmt.Errorf("failed to read screen config file: %w", err)
	}

	err = yaml.Unmarshal(configFileData, &screenConfig)
	if err != nil {
		return fmt.Errorf("failed to parse screen config file: %w", err)
	}

	return nil
}

var ErrMissingDataFile = errors.New("missing data file path. Please run again with --data defined")

func ParseDataConfig(cmd *cobra.Command, args []string) error {
	configFilePath := viper.GetString("data")
	if configFilePath == "" {
		return ErrMissingDataFile
	}

	configFileData, err := os.ReadFile(configFilePath)
	if err != nil {
		return fmt.Errorf("failed to read data config file: %w", err)
	}

	err = yaml.Unmarshal(configFileData, &data)
	if err != nil {
		return fmt.Errorf("failed to parse data config file: %w", err)
	}

	return nil
}

var rootCmd = &cobra.Command{
	Use:     "eink-radiator",
	Short:   "A brief description of your application",
	PreRunE: RunSerially(ParseDataConfig, ParseScreenConfig),
	RunE: func(cmd *cobra.Command, args []string) error {
		// fmt.Printf("port is %d\n", viper.GetInt("port"))
		rotation := &internal.Rotation{
			ImageConfigs: data.Rotation,
		}
		rotation.Start()

		return nil
	},
}

func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

var (
	cfgFile      string
	data         *internal.Data
	screenConfig *pkg.ScreenConfig
)

const (
	DefaultPort = 8000
)

func init() {
	cobra.OnInitialize(initConfig)

	rootCmd.Flags().StringVar(&cfgFile, "config", "", "config file path")
	rootCmd.Flags().IntP("port", "p", DefaultPort, "The port number to listen on for the HTTP API and browser UI")
	rootCmd.Flags().StringP("data", "d", "", "The path to the data config file")
	rootCmd.Flags().StringP("screen", "s", "", "The path to the screen config file")

	_ = viper.BindPFlag("port", rootCmd.Flags().Lookup("port"))
}

func initConfig() {
	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath(".")
	viper.AddConfigPath("configs")

	if cfgFile != "" {
		viper.SetConfigFile(cfgFile)
	}

	viper.SetEnvPrefix("eink_radiator")
	viper.AutomaticEnv()

	if err := viper.ReadInConfig(); err == nil {
		fmt.Fprintln(os.Stderr, "Using config file:", viper.ConfigFileUsed())
	}
}
