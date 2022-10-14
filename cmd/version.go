package cmd

import (
	"github.com/spf13/cobra"
)

var Version = "dev"
var VersionCmd = &cobra.Command{
	Use:   "version",
	Short: "Print the version of the eink-radiator",
	Run: func(cmd *cobra.Command, args []string) {
		cmd.Printf("eink-radiator version: %s\n", Version)
	},
}

func init() {
	rootCmd.AddCommand(VersionCmd)
	VersionCmd.SetOut(VersionCmd.OutOrStdout())
}
