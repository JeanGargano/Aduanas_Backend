from pydantic import BaseModel
from typing import Optional
from datetime import date

class PedidoModel(BaseModel):
    id_pedido: Optional[int] = None
    id_cliente: int
    fecha_arribo: Optional[date] = None
    fecha_entrega_transporte: Optional[date] = None
    radicado_dim: Optional[int] = None
    numero_aceptacion: Optional[int] = None
    fecha_aceptacion: Optional[date] = None
    sticker: Optional[str] = None
    dec_valor: Optional[str] = None
    proveedor: Optional[str] = None
    numero_contrato: Optional[str] = None
    producto: Optional[str] = None
    numero_factura: Optional[str] = None
    fecha_factura: Optional[str] = None
    numero_lista_empaque: Optional[str] = None
    tipo_empaque: Optional[str] = None
    certificado_sanitario: Optional[str] = None
    lote: Optional[str] = None
    fecha_vencimiento: Optional[str] = None
    radicado_invima: Optional[str] = None
    llave: Optional[int] = None
    fecha_radicado_invima: Optional[date] = None
    numero_solicitud_invima: Optional[str] = None
    numero_certificado_invima: Optional[int] = None
    fecha_certificado_invima: Optional[date] = None
    registro_de_importacion: Optional[str] = None
    fecha: Optional[date] = None
    bl: Optional[str] = None
    naviera: Optional[str] = None
    moto_nave: Optional[str] = None
    bandera: Optional[str] = None
    viaje: Optional[str] = None
    contenedor: Optional[str] = None
    peso: Optional[int] = None
    manifiesto: Optional[int] = None
    puerto_arribo: Optional[str] = None
    fecha_llegada: Optional[date] = None
    dias_libres: Optional[int] = None
    observaciones: Optional[str] = None
    entrega_transporte: Optional[str] = None
    estado: Optional[str] = "EN PROCESO"



class Pedido_estado(BaseModel):
    id_pedido: int
    nuevo_estado: str

    
    
