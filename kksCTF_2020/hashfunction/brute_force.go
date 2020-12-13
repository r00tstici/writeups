package main

import (
	"encoding/hex"
	"fmt"
)

var table_1 = [256]uint32{0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501, 0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821, 0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x2441453, 0xd8a1e681, 0xe7d3fbc8, 0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a, 0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70, 0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x4881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665, 0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1, 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391, 0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501, 0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821, 0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x2441453, 0xd8a1e681, 0xe7d3fbc8, 0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a, 0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70, 0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x4881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665, 0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1, 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391, 0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501, 0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821, 0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x2441453, 0xd8a1e681, 0xe7d3fbc8, 0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a, 0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70, 0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x4881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665, 0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1, 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391, 0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501, 0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821, 0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x2441453, 0xd8a1e681, 0xe7d3fbc8, 0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a, 0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70, 0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x4881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665, 0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1, 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391}
var table_2 = [256]uint32{0xd76aa478, 0xec06aae1, 0x2da24bb5, 0xccfee837, 0xe6787973, 0x5042ad41, 0xb2b60ba1, 0xe301c504, 0x4f887560, 0xa98d07a0, 0xd0758d67, 0xa2171cdf, 0x5e9c8a46, 0xcc55f740, 0x9af7e384, 0x71fbb59c, 0xba0ffe12, 0x88907587, 0x63cdba4f, 0xa8e43a03, 0x893abdf1, 0x5990a448, 0x8e367043, 0xb58570bd, 0x4bf8fb2e, 0xadef2ca9, 0x974e0021, 0x220004fc, 0xd0fea911, 0x8133fe5b, 0x17f079a3, 0xf9742a47, 0x67d98fa2, 0x1b935dd6, 0xfc3cecac, 0x6885a835, 0x2f992a78, 0xc4381222, 0x741eb032, 0x38db5a95, 0x96b0259e, 0x504b6115, 0x634650b3, 0xb7e06084, 0x74fbfdbd, 0x4f35a9d6, 0xbb0f6a12, 0x64c05d38, 0x201b4fd4, 0x93d98fb0, 0x76247559, 0x25e2eb70, 0xa26d428f, 0x4cfbca69, 0x315bd45f, 0x4ff16044, 0x9d92fe67, 0x8d77b7f, 0x58b9f852, 0xb171b750, 0x166d8876, 0x58c51976, 0xc26b1f21, 0x7fb03bc, 0xe3ecd40f, 0xd880da96, 0x19243bc2, 0xf8789840, 0xd2fe0904, 0x64c4dd36, 0x86307bd6, 0xd787b573, 0x7b0e0517, 0x9d0b77d7, 0xe4f3fd10, 0x96916ca8, 0x6a1afa31, 0xf8d38737, 0xae7193f3, 0x457dc5eb, 0x8e898e65, 0xbc1605f0, 0x574bca38, 0x9c624a74, 0xbdbccd86, 0x6d16d43f, 0xbab00034, 0x810300ca, 0x7f7e8b59, 0x99695cde, 0xa3c87056, 0x1686748b, 0xe478d966, 0xb5b58e2c, 0x237609d4, 0xcdf25a30, 0x535fffd5, 0x2f152da1, 0xc8ba9cdb, 0x5c03d842, 0x1b1f5a0f, 0xf0be6255, 0x4098c045, 0xc5d2ae2, 0xa23655e9, 0x64cd1162, 0x57c020c4, 0x836610f3, 0x407d8dca, 0x7bb3d9a1, 0x8f891a65, 0x50462d4f, 0x149d3fa3, 0xa75fffc7, 0x42a2052e, 0x11649b07, 0x96eb32f8, 0x787dba1e, 0x5dda428, 0x7b771033, 0xa9148e10, 0x3c510b08, 0x6c3f8825, 0x85f7c727, 0x22ebf801, 0x6c436901, 0xf6ed6f56, 0x337d73cb, 0xbe664496, 0x850a4a0f, 0x44aeab5b, 0xa5f208d9, 0x8f74999d, 0x394e4daf, 0xdbbaeb4f, 0x8a0d25ea, 0x2684958e, 0xc081e74e, 0xb9796d89, 0xcb1bfc31, 0x37906aa8, 0xa55917ae, 0xf3fb036a, 0x18f75572, 0xd3031efc, 0xe19c9569, 0xac15aa1, 0xc1e8daed, 0xe0365d1f, 0x309c44a6, 0xe73a90ad, 0xdc899053, 0x22f41bc0, 0xc4e3cc47, 0xfe42e0cf, 0x4b0ce412, 0xb9f249ff, 0xe83f1eb5, 0x7efc994d, 0x9078caa9, 0xed56f4c, 0x729fbd38, 0x95300c42, 0x18948db, 0x4695ca96, 0xad34f2cc, 0x1d1250dc, 0x51d7ba7b, 0xffbcc570, 0x394781fb, 0xa4ab05d, 0xdeec806a, 0x1df71d53, 0x26394938, 0xd2038afc, 0xdccbdd6, 0x4917af3a, 0xfad56f5e, 0x1f2895b7, 0x4cee0b9e, 0xcb61a261, 0x25f72a87, 0x585734b1, 0x26fd80aa, 0xf49e1e89, 0x61db9b91, 0x31b518bc, 0xd87d57be, 0x7f616898, 0x31c9f998, 0xab67ffcf, 0x6ef7e352, 0x8ae034e1, 0xb18c3a78, 0x7028db2c, 0x917478ae, 0xbbf2e9ea, 0xdc83dd8, 0xef3c9b38, 0xbe8b559d, 0x1202e5f9, 0xf4079739, 0x8dff1dfe, 0xff9d8c46, 0x3161adf, 0x91df67d9, 0xc77d731d, 0x2c712505, 0xe7856e8b, 0xd51ae51e, 0x3e472ad6, 0xf56eaa9a, 0xd4b02d68, 0x41a34d1, 0xd3bce0da, 0xe80fe024, 0x16726bb7, 0xf065bc30, 0xcac490b8, 0x7f8a9465, 0x8d743988, 0xdcb96ec2, 0x4a7ae93a, 0xa4febade, 0x3a531f3b, 0x4619cd4f, 0xa1b67c35, 0x350f38ac, 0x7213bae1, 0x99b282bb, 0x299420ab, 0x6551ca0c, 0xcb3ab507, 0xdc1f18c, 0x3eccc02a, 0xea6af01d, 0x29716d24, 0x12bf394f, 0xe685fa8b, 0x394acda1, 0x7d91df4d, 0xce531f29, 0x2baee5c0, 0x78687be9, 0xffe7d216, 0x11715af0, 0x6cd144c6, 0x127bf0dd, 0xc0186efe, 0x555debe6, 0x53368cb, 0xecfb27c9, 0x4be718ef, 0x54f89ef, 0x9fe18fb8, 0x5a719325}
var table [256]uint32

func initMD5() {
	for i := 0; i < 256; i++ {
		table[i] = table_1[i] ^ table_2[i]
	}
}

func MD5(psw string) string {
	data := []byte(psw)
	var F uint32

	F = ^F
	for i := 0; i < 4; i++ {
		F = (F << 8) ^ table[(F>>24)^(uint32(data[i])&0xff)]
	}
	F = ^F
	
	var digest [4]byte

	digest[3] = byte((F >> 24) & 0xff)
	digest[2] = byte((F >> 16) & 0xff)
	digest[1] = byte((F >> 8) & 0xff)
	digest[0] = byte(F & 0xff)

	return hex.EncodeToString(digest[:])
}

func main() {
	printables := "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\\'()*+,-./:;<=>?@[\\]^_`{|}~ "
	initMD5()
	
	for _, a := range printables {
		for _, b := range printables {
			for _, c := range printables {
				for _, d := range printables {
					str := string(a)+string(b)+string(c)+string(d)
					digest := MD5(str)

					if digest == "90829146" {
						fmt.Println("1\t" + digest + "\t" + str)
					} else if digest == "b3603e2e" {
						fmt.Println("2\t" + digest + "\t" + str)
					} else if digest == "7daf5031" {
						fmt.Println("3\t" + digest + "\t" + str)
					} else if digest == "b2103e9e" {
						fmt.Println("4\t" + digest + "\t" + str)
					}
				}
			}
		}	
	}	
}