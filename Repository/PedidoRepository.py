import mysql.connector
from typing import List, Optional
from Model.PedidoModel import PedidoModel
from configurations import settings
import logging
from Repository.BaseRepository import BaseRepository
from fastapi import Depends

logger = logging.getLogger(__name__)

class PedidoRepository(BaseRepository):

    #Inicializacion de la conexión
    def __init__(self):
        logger.info("PedidoRepository inicializado")
    
    def crear_pedido(self, pedido: PedidoModel) -> Optional[PedidoModel]:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            campos = [
                "id_cliente", "fecha_arribo", "fecha_entrega_transporte", "radicado_dim",
                "numero_aceptacion", "fecha_aceptacion", "sticker", "dec_valor", "proveedor",
                "numero_contrato", "producto", "numero_factura", "fecha_factura",
                "numero_lista_empaque", "tipo_empaque", "certificado_sanitario", "lote",
                "fecha_vencimiento", "radicado_invima", "llave", "fecha_radicado_invima",
                "numero_solicitud_invima", "numero_certificado_invima", "fecha_certificado_invima",
                "registro_de_importacion", "fecha", "bl", "naviera", "moto_nave", "bandera",
                "viaje", "contenedor", "peso", "manifiesto", "puerto_arribo", "fecha_llegada", "dias_libres",
                "observaciones", "entrega_transporte"
            ]

            # Genera placeholders (%s, %s, ..., %s)
            placeholders = ', '.join(['%s'] * len(campos))

            # Construye SQL dinámicamente
            sql = f"""
                INSERT INTO Pedido ({', '.join(campos)})
                VALUES ({placeholders})
            """

            # Extrae los valores del modelo
            valores = tuple(getattr(pedido, campo) for campo in campos)

            cursor.execute(sql, valores)
            conn.commit()

            pedido.id_pedido = cursor.lastrowid
            logger.info(f"Pedido creado con ID: {pedido.id_pedido}")
            return pedido

        except Exception as e:
            logger.exception(f"Error al crear pedido: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()


    def listar_pedidos(self) -> List[PedidoModel]:
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Pedido")
            rows = cursor.fetchall()
            pedidos = [PedidoModel(**row) for row in rows]
            return pedidos
        except Exception as e:
            logger.exception(f"Error al listar los pedidos: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()


    def listar_pedidos_del_cliente(self, id_cliente: int) -> List[PedidoModel]:
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM Pedido WHERE id_cliente = %s", (id_cliente,))
            rows = cursor.fetchall()
            pedidos = [PedidoModel(**row) for row in rows]
            return pedidos

        except Exception as e:
            logger.exception(f"Error al listar pedidos del cliente: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()


    def actualizar_pedido_por_id(self, id_pedido: int, datos_actualizados: dict) -> bool:
        try:
            if not datos_actualizados:
                logger.warning("No se proporcionaron datos para actualizar")
                return False
            conn = self.get_connection()
            cursor = conn.cursor()
            # Armamos el SQL dinámicamente
            campos = ', '.join(f"{k} = %s" for k in datos_actualizados.keys())
            valores = list(datos_actualizados.values())
            valores.append(id_pedido)

            sql = f"UPDATE Pedido SET {campos} WHERE id_pedido = %s"
            cursor.execute(sql, valores)
            logger.info(f"SQL: {sql}")
            logger.info(f"Valores: {valores}")
            conn.commit()

            actualizado = cursor.rowcount > 0
            if actualizado:
                logger.info(f"Pedido con ID {id_pedido} actualizado")
            else:
                logger.info(f"No se encontró pedido con ID {id_pedido} para actualizar")
            return actualizado

        except Exception as e:
            logger.exception(f"Error al actualizar pedido: {str(e)}")
            return False
        finally:
            cursor.close()
            conn.close()

    def actualizar_estado(self, id_pedido: int):
        pass

