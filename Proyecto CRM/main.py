## File: main.py
# This is the main entry point for the CRM console application.
def main():
    while True:
        print("\n=== SISTEMA CRM ===")
        print("1. Registrar nuevo usuario")
        print("2. Buscar usuario")
        print("3. Crear factura para usuario")
        print("4. Mostrar todos los usuarios")
        print("5. Mostrar facturas de un usuario")
        print("6. Resumen financiero por usuario")
        print("7. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            from controllers import usuario_controller
            usuario_controller.registrar_usuario()
        elif opcion == "2":
            from controllers import usuario_controller
            usuario_controller.buscar_usuario()
        elif opcion == "3":
            from controllers import factura_controller
            factura_controller.crear_factura()
        elif opcion == "4":
            from controllers import usuario_controller
            usuario_controller.mostrar_todos_usuarios()
        elif opcion == "5":
            from controllers import factura_controller
            factura_controller.mostrar_facturas_por_usuario()
        elif opcion == "6":
            from controllers import reportes_controller
            reportes_controller.mostrar_resumen_financiero()
        elif opcion == "7":
            print("¡Hasta pronto!")
            break
        else:
            print("❌ Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    main()
