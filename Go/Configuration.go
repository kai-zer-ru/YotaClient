package main

import (
	"io/ioutil"
	"fmt"
	"bytes"
	"strconv"
	"strings"
)
type Config struct {
	Configuration_filename string
	Configuration map[string]string
}

//------------------------------------------------------------------------------
// readConfiguration читает конфигурацию из файла
func (Conf *Config)ReadConfiguration() bool {
	file_content, err := ioutil.ReadFile (Conf.Configuration_filename)
	if err != nil {
		return false
	}

	// Читаем конфигурацию из файла.
	lines := bytes.Split (file_content, []byte{'\n'})

	for _, line := range lines {
		if (len(line) <= 1) {
			continue
		}
		if (line[0] == '#') {
			continue
		}

		name_value := bytes.Split (line, []byte{'='})

		if len(name_value) != 2 && len(name_value[0]) != 0 {
			fmt.Println ("Error. Wrong format of configuration file")
			return false
		}

		name := string(bytes.Trim(name_value[0], " "))

		if (len(name)>0) {
			value := string(bytes.Trim(name_value[1], " "))
			Conf.Configuration[name] = value
		}
	}

	return true
}

//------------------------------------------------------------------------------
// getConfUint32 возвращает значение из конфигурации, если оно присутсвует
//               иначе возвращате default_value
func (Conf *Config) GetConfUint32(name string, default_value uint32) uint32{
	temp_str, ok := Conf.Configuration[name]

	if !ok {
		return default_value
	}

	temp_uint, err := strconv.ParseUint(strings.Trim(temp_str, " "), 10, 32)
	if err != nil {
		fmt.Printf ("Error. Incorect value of \"%s\"", name)
		return default_value
	}
	return uint32(temp_uint)
}


//------------------------------------------------------------------------------
// getConfString возвращает значение из конфигурации, если оно присутсвует
//               иначе возвращате default_value
func (Conf *Config) GetConfString(name string, default_value string) string {
	temp_str, ok := Conf.Configuration[name]

	if !ok {
		return default_value
	}

	return string(temp_str)
}
