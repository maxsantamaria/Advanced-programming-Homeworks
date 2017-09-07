from form import FormRegister


if __name__ == '__main__':
    form = FormRegister()

    with open("test.txt") as test_file:

        for line in test_file:
            name, gender, rut, course, section, comment = line.split(";")
            comment = comment.strip("\n")

            try:

                rut_verified = form.check_rut(rut)
            except TypeError as e:
                rut_corregido = ""
                for i in range(0, len(rut)):
                    if rut[i] != ".":  # sacamos puntos
                        rut_corregido += rut[i]
                rut_corregido = rut_corregido.replace(" ", "-")  # espacios por guiones
                rut = rut_corregido

                rut_verified = form.check_rut(rut)


            if rut_verified:
                try:
                    form.add_course(course, section)
                except TypeError as e:
                    course_corregido = ""
                    for letra in course:
                        if letra != " ":
                            course_corregido += letra
                    course = course_corregido
                    course = course.strip()


                except NameError as e:
                    section = section[7:]
                except ValueError as e:
                    section = "0"

                try:
                    form.add_course(course, section)
                except NameError as e:
                    section = section[7:]
                except ValueError as e:
                    section = "0"


                form.register_people_info(name, gender, comment)
            print(rut, course, section)

        form.save_data("result.txt")