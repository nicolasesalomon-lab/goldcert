from alembic import op
import sqlalchemy as sa
revision = '0001_init_v2'
down_revision = None
branch_labels = None
depends_on = None
def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False, server_default='admin')
    )
    op.create_table('proveedores',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('nombre', sa.String(length=200), nullable=False, unique=True),
        sa.Column('contacto_email', sa.String(length=255)),
        sa.Column('contacto_telefono', sa.String(length=50)),
    )
    op.create_table('fabricas',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('proveedor_id', sa.Integer(), sa.ForeignKey('proveedores.id'), nullable=False),
        sa.Column('direccion', sa.String(length=255)),
    )
    op.create_table('auditorias_fabrica',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('fabrica_id', sa.Integer(), sa.ForeignKey('fabricas.id'), nullable=False),
        sa.Column('fecha_auditoria', sa.Date(), nullable=False),
        sa.Column('fecha_vencimiento', sa.Date(), nullable=False),
    )
    op.create_table('productos',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('nombre', sa.String(length=200), nullable=False),
        sa.Column('categoria', sa.String(length=120)),
        sa.Column('marca', sa.String(length=120)),
        sa.Column('origen', sa.String(length=120)),
        sa.Column('proveedor_id', sa.Integer(), sa.ForeignKey('proveedores.id'), nullable=False),
    )
    op.create_table('modelos_proveedor',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('producto_id', sa.Integer(), sa.ForeignKey('productos.id'), nullable=False),
        sa.Column('codigo_proveedor', sa.String(length=120), nullable=False),
    )
    op.create_table('modelos_producto',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('modelo_proveedor_id', sa.Integer(), sa.ForeignKey('modelos_proveedor.id'), nullable=False),
        sa.Column('codigo_goldmund', sa.String(length=120), nullable=False),
    )
    op.create_table('variaciones_esteticas',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('producto_id', sa.Integer(), sa.ForeignKey('productos.id'), nullable=False),
        sa.Column('nombre_grupo', sa.String(length=200), nullable=False),
    )
    op.create_table('variacion_modelos',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('variacion_id', sa.Integer(), sa.ForeignKey('variaciones_esteticas.id'), nullable=False),
        sa.Column('modelo_producto_id', sa.Integer(), sa.ForeignKey('modelos_producto.id'), nullable=False),
    )
    op.create_table('tipos_certificacion',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('nombre', sa.String(length=50), nullable=False, unique=True),
        sa.Column('descripcion', sa.Text()),
    )
    op.create_table('certificados',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('producto_id', sa.Integer(), sa.ForeignKey('productos.id'), nullable=False),
        sa.Column('tipo_certificacion_id', sa.Integer(), sa.ForeignKey('tipos_certificacion.id'), nullable=False),
        sa.Column('ambito_certificado', sa.String(length=10)),
        sa.Column('modelo_proveedor_id', sa.Integer(), sa.ForeignKey('modelos_proveedor.id'), nullable=False),
        sa.Column('fabrica_id', sa.Integer(), sa.ForeignKey('fabricas.id'), nullable=False),
        sa.Column('tipo_ensayo', sa.String(length=120)),
        sa.Column('test_report', sa.String(length=200)),
        sa.Column('fecha_emision', sa.Date(), nullable=False),
        sa.Column('fecha_vencimiento', sa.Date(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='draft'),
    )
    op.create_table('attachments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('object_type', sa.String(length=40), nullable=False),
        sa.Column('object_id', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(length=40), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('path', sa.String(length=500), nullable=False),
        sa.Column('mime_type', sa.String(length=120)),
        sa.Column('size', sa.Integer()),
    )
    op.create_table('declaraciones_juradas',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('numero', sa.String(length=50), nullable=False, unique=True),
        sa.Column('fecha_generacion', sa.Date(), nullable=False),
        sa.Column('plantilla', sa.Text()),
    )
    op.create_table('declaracion_modelos',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('declaracion_id', sa.Integer(), sa.ForeignKey('declaraciones_juradas.id'), nullable=False),
        sa.Column('modelo_producto_id', sa.Integer(), sa.ForeignKey('modelos_producto.id'), nullable=False),
    )
def downgrade():
    op.drop_table('declaracion_modelos')
    op.drop_table('declaraciones_juradas')
    op.drop_table('attachments')
    op.drop_table('certificados')
    op.drop_table('tipos_certificacion')
    op.drop_table('variacion_modelos')
    op.drop_table('variaciones_esteticas')
    op.drop_table('modelos_producto')
    op.drop_table('modelos_proveedor')
    op.drop_table('productos')
    op.drop_table('auditorias_fabrica')
    op.drop_table('fabricas')
    op.drop_table('proveedores')
    op.drop_table('users')
