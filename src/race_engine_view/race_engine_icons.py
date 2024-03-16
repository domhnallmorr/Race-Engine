from PIL import Image, ImageTk
import base64
import io

import customtkinter

def setup_icons(view):

	size = 18,18

	data = "iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAACLUlEQVR4nO3dMYoUQRTG8RZRERQ2EQ011sQLeItNDb2CeIMVFTHcK3iF3guMuRNPMGuwywTiJj3g/E16QBBl131Vr96r73eCqo+G7q/7FT0MIiIiIiIiGQG3gbfAN+Ac+Ag88F5XOsARf/oOvAHueq8vjflK/ps18Aq46b3O8LicJXDovdYegt4bgefeaw6Jq9sBn4En3mvPHvTeBHwCDrz3EALXtwFeA3e895I96L0V8BK44b2nJmFvAbzw3lcPQf/+hPLMe3/NoKwtcAw8HHpHHRdz1b8/9Iq61t1Wenwsu6v0+DrpptLjb9dFpacdU+pKT3s2KSs97VqlqvS0b5Gi0hPHGLrSE8t2rvSPhmiI6SJcpSe2dZhKTw7L5is9uZw0W+nJZ9dkpSevqalKT36bJio9/Vi5Vnr688Wl0tOvsWqlp2/befD+loKu472CruNcQdehoCt5pyu6/M3wg26GZenxrjAVlsJUwQvTS6XC9Jq0ML34r0CfsgrTx9nCNG5QmAZoCot7yos4Rg05lqWx3cI0iN5FZbZGO6amJouseadLq5XZmnPIY7PTn9acAl42P89srXLA6zAT+tYqBfxjPnNyb+hV4YC3YSuztcI3uqfe+2tGgYAXKU66WjMMeJXq7LY1g4A3KSuztWsEPKWuzNb+I+Cfc2V+7L32UK4Y8thNZbZ2yYC/dleZrQGn/wi438psTT9TqPt7kKP5yj7T70FERERERESGeH4Ba6DZnW6HaMEAAAAASUVORK5CYII="
	view.play_icon2 = customtkinter.CTkImage(light_image=decode_base64_image(size, data), size=size)

	data = "iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAACXBIWXMAAAsTAAALEwEAmpwYAAABe0lEQVR4nO3QwYkDQBDEwM0/afl97zNUG6YSEOi9c84555xzzjnnnHPOOeec8y992fux/hw9JNyfo4eE+3P0kHB/jh4S7s/RQ8L9OXpIuD9HDwn35+gh4f4cPSTcn6OHhPtz9JBwf44eEu7P0UPC/Tl6SLg/Rw8J9+foIeH+HD0k3J+jh4T7c/SQcH+OHhLuz9FDwv05eki4P0cPCffn6CHh/hw9JNyfo4eE+3P0kHB/jh4S7s/RQ8L9OXpIuD9HDwn35+gh4f4cPSTcn6OHhPtz9JBwf44eEu7P0UPC/Tl6SLg/Rw8J9+foIeH+HD0k3J+jh4T7c/SQcH+OHhLuz9FDwv05eki4P0cPCffn6CHh/hw9JNyfo4eE+3P0kHB/jh4S7s/RQ8L9OXpIuD9HDwn35+gh4f4cPSTcn6OHhPtz9JBwf44eEu7P0UPC/Tl6SLg/Rw8J9+foIeH+HD0k3J+jh4T7c/SQcP+cc84555xzzjnnnHPOOee8Pz5RNVf3BytRbQAAAABJRU5ErkJggg=="
	view.pause_icon2 = customtkinter.CTkImage(light_image=decode_base64_image(size, data), size=size)

	data = "iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAACXBIWXMAAAsTAAALEwEAmpwYAAAFLklEQVR4nO2d24tVVRzHV3cr06KaqaywC9H1QVPrLygIKhGrh0AU6WI+1INYQg+99RAlBj0kjI6mXShyuhIElWlpEvqYRY+O9FA2NmEt8viJHy5hms44e8+ss9d37b0/T4fDOWf/1vqcvdba6+pcS0tLS0tLw2ASUsfXOGiFaIGgEOAx4HXgDNc0EBMSZJwIl9/YOCkICRkng0ZKQUTIBDKaJwUBIZPIaJYUEgsB7i8g4xSv1UoKcD3wELAOGAB2FsiEneGzzwFL7Tcix3Qu8FFBIXlLAeYAq4A3gUPEw35rO/AkcFWEOOsrBbg8SPgK6NB77BpfBjmXTiPuB0ped4lTBrgR2AAcIx1/A1uB20rGfg/wV4nrvOJUAe4EPi5RMVLRXWNF0LwC8d9bUsbLTrh+GKyoWJoqFtum09UzwNAE39ufhQzgLOBZ4E/yYRRYA5zZJT0zgM/GyVjZpaKXlDG3YFNVlW+truuSrlOZb8XuqnHvD0nWGcCy8E/LnT+ARye4U+7r8v45TglrbwMvUD82dCvCpAFmTlDp1YVPgVkuB4DZwF7qz/fAJS4DGd9VnDE7gD6gP7yukj2ydwpwUaI7o29MDCaFBFJmOiWskktUZ/gusfgEcXxiz1lOBeAl0uBFhBgvOqHnjFR4ISF0e06pFOC68MCUCi8mZLTbE32V9Ubq7hAvJsTYnaQ+CUOjqfGCQow1KbrQFXptvaiQ0RhDxGWEvIEGXlSIsakqGfOFBpe8sBDLowVVCBk7KJMaLyzE+LDXMm4XGwP34kIsr27tpRAbZ1bCiwsxNvZy3pRNl1HCZyDEZqZc1gshq9HDZyDEeKIXQnahh89EyBexZVwj1NTNUYjl3ZyYQp5CE5+JkLjFFvAOmviMhGyPKWQYTXxGQg7FknETuviMhBBl0RDwCLr4zIQsjSHkeXTxmQlZF0OILR1AtCm5uUu8m0Wb6HG65IFv0OM3YNFpYr4bOIIeu2II+Rkt/gEWFoj7LuA4WvwUQ8gvaDGQcXF7OIYQtbUdC0vEbneJEqMxpvooDUgZ55eI/wK06ExrnXpYdNPJWMiF1ElISFTKmYl1K7KOTktGSNRhMm3LA1uoW38W8CN6zd5FmTZ7f4ghxJYEq3HEMjzDB8PdMYSoteUn6zoZrHvXie1RpYrPrHNxbQwhS9DFZybkwRhC2gGqeMRZzNMO4UZhOIqMIGQbuvQlXhZdlK0xhdi2Q6rsCCL6xbfzWB5TyLWCnYw5Yc3wq6MJCVK+Tp2qjIk7lXTMLs4tU2NFL4TMSrxzaK5Yns2OLiRIsa1UW8rxv+6dmEJuEe4nUqRTdi/gqUh5P3UqM+LtnsoIQua1TeBC2GPC/J4LCVLeKhZTo9lSiYwg5ApgJHWKhTkKXFmZkCDlmdSpFmZ1pTKCkLOBfalTLsjeZNv9ATe0Rdd/+N02dUsiY4wUO06oRemwFuDVEFCTWe/EjqJ4j+bygdWpTgmbcyuwB2MK7MysGU4R4GLgAM3hgKXZKROkNOFO2TOd090qBTgPeJf6MlRmWYRSRW+Hn9Stw3C91D7vZQEWi058nkr/1MOuRmfZ7su8O2SuqxNhvaJt3P8r+TACPJ11EVWw636b+DyvE2H+QL9rCsAdIdHHBY9eXeCaSpg4MZh4itGxsEfKzanzQ4Yw72sZ8HlFxVknHC3xuOzBXipwctPNFaFIG458wL395vLoc22bBCfPXF8cDjceCP/sgyGDx47tj4T3DoZtbe2za8N305x809LS0tLS4qrhXzpV0RcxhLM4AAAAAElFTkSuQmCC"
	view.stopwatch_icon2 = customtkinter.CTkImage(light_image=decode_base64_image(size, data), size=size)

	data= "iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAACXBIWXMAAAsTAAALEwEAmpwYAAABDklEQVR4nO3dwQ3CQBAEwQsPyD8CCGSR3/6BJbetqgBOo+0Abi0AAICYmXnNzGei1n5v1XbD5xFBsjEuFmTzPiJI2rr4XkFOJkiMIDGCxAgSI0iMIDGCxAgSI0iMIDGCxAgSI0iMIDGCxAgSI0iMIDGCxAgSI0iMIHcLAgC/mrh18b2CnEyQGEFiBIkRJEaQGEFiBIkRJEaQGEFiBIkRJEaQGEFiBIkRJEaQGEFiBIkRJEaQGEHuFgQAfjVx6+J7BTmZIDGCxAgSI0iMIDGCxAgSI0iMIDGCxAgSI0iMIDGCxAgSI0iMIDGCxAgSI0iMIDGC3DCID+5jH9w/t4cmau33Vm03fPwdBAAAYB3rCwuHoscz8qtzAAAAAElFTkSuQmCC"
	view.timing_icon2 = customtkinter.CTkImage(light_image=decode_base64_image(size, data), size=size)

	data = "iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAACdklEQVR4nO2cTU7DMBBGZ1W4DD9nKwuWyZJjFHoDFlXPUzhGqg8ZORKUluZnPJlJvrcG9fnJmCSNLUIIIYQQQgghSwFADeBFgoII/lmyxbdsVP8TSd+yUf0vSPqUjep/RdKXbFT/jpJuY4fw7ynpLnYI/4GSLWtT2fP+TxhOHSFyogFwbyJ73v8xO8BtbIXILa9FRf8fwxY61N4jJz6KSHYbxyf0qD1HTjSqgv3GMnbZKBcbwLOyHNTk+o9Fm0pbUDW2TITryCViy0S4j6wdWyYiRGTlf443JrK/vW8UvGtr6bEzew/g1tB3BeA9xEyOGhuRI/8YxHrktemu5DKSl4v0GUNpPDyf+SY9u0i31emOb2D0XYnYIyKnMRwAbADcSRTQ7U9XdRmZ4jNdAMOBLzayZYDFR7YIwcgGQRjZIAyWviZbBAIjl48NRi4/s8HIw0CPcIxsc8u86/gz5o9hQ4HxT9qWe3VhGJuRDWIzskFsRh4DGLo84NLhMnILl5Cu8PLOAPCGxSTyirfgjiLLiN9ZNOBjUt+RWzizrwB+lVUe8MvZmJFbuIxk+AKNAeArYfOKPOtlJG/73ebNkkfEf233mMfyBuBBPJA3sPNFdOebhvaBtlaEOq8j+mahUOd1tHD7m0FkmM2Kv/4alJ3ZmqccyERo+ReLrX2UhEyE5hjUYxc4rwOqgv3GArexeTBK3FNoDqpycznqp0DsTRHBbmNIt9UauD8prJly2296duH+OLYZHTC4dh955BESlTghlH9P2UqcEcq/o2wlTgnlf0W2EueE8r8g60tyLv4nsj4l5+KfL/1sL4EUie5PCCGEEEIIIdKXL/FeSve/F5iQAAAAAElFTkSuQmCC"
	view.pit_icon2 = customtkinter.CTkImage(light_image=decode_base64_image(size, data), size=size)


def decode_base64_image(size, data):

	# msg = base64.b64decode(data)
	# buf = io.BytesIO(msg)
	
	# i = Image.open(buf)
	# i.thumbnail(size, Image.ANTIALIAS)
	
	# # adding transparent padding before text
	# new_image = Image.new('RGBA', (size[0]+5, size[1]), (0, 0, 0, 0))
	# new_image.paste(i, (0, 0))
	
	# return new_image

	im = Image.open(io.BytesIO(base64.b64decode(data)))

	return im