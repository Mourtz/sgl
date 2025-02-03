// SPDX-License-Identifier: Apache-2.0

#include "nanobind.h"

#include "sgl/device/coopvec.h"
#include "sgl/device/command.h"

#include "sgl/device/resource.h"

#include <iostream>

SGL_PY_EXPORT(device_coopvec)
{
    using namespace sgl;

    nb::sgl_enum<CoopVecMatrixLayout>(m, "CoopVecMatrixLayout", D_NA(CoopVec, MatrixLayout));

    nb::class_<CoopVecMatrixDesc>(m, "CoopVecMatrixDesc", D_NA(CoopVec, MatrixDesc))
        .def(nb::init<>())
        .def(
            "__init__",
            [](CoopVecMatrixDesc* self,
               uint32_t rows,
               uint32_t cols,
               DataType element_type,
               CoopVecMatrixLayout layout,
               size_t size,
               size_t offset)
            {
                self->rows = rows;
                self->cols = cols;
                self->element_type = element_type;
                self->layout = layout;
                self->size = size;
                self->offset = offset;
            },
            "rows"_a,
            "cols"_a,
            "element_type"_a,
            "layout"_a,
            "size"_a,
            "offset"_a
        )
        .def_rw("rows", &CoopVecMatrixDesc::rows, D_NA(CoopVec, MatrixDesc, rows))
        .def_rw("cols", &CoopVecMatrixDesc::cols, D_NA(CoopVec, MatrixDesc, cols))
        .def_rw("element_type", &CoopVecMatrixDesc::element_type, D_NA(CoopVec, MatrixDesc, element_type))
        .def_rw("layout", &CoopVecMatrixDesc::layout, D_NA(CoopVec, MatrixDesc, layout))
        .def_rw("size", &CoopVecMatrixDesc::size, D_NA(CoopVec, MatrixDesc, size))
        .def_rw("offset", &CoopVecMatrixDesc::offset, D_NA(CoopVec, MatrixDesc, offset));
}
