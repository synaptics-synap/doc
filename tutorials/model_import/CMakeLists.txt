#
# NDA AND NEED-TO-KNOW REQUIRED
#
# Copyright (C) 2022-2023 Synaptics Incorporated. All rights reserved.
#
# This file contains information that is proprietary to Synaptics
# Incorporated ("Synaptics"). The holder of this file shall treat all
# information contained herein as confidential, shall use the
# information only for its intended purpose, and shall not duplicate,
# disclose, or disseminate any of this information in any manner
# unless Synaptics has otherwise provided express, written
# permission.
#
# Use of the materials may require a license of intellectual property
# from a third party or from Synaptics. This file conveys no express
# or implied licenses to any intellectual property rights belonging
# to Synaptics.
#
# INFORMATION CONTAINED IN THIS DOCUMENT IS PROVIDED "AS-IS", AND
# SYNAPTICS EXPRESSLY DISCLAIMS ALL EXPRESS AND IMPLIED WARRANTIES,
# INCLUDING ANY IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE, AND ANY WARRANTIES OF NON-INFRINGEMENT OF ANY
# INTELLECTUAL PROPERTY RIGHTS. IN NO EVENT SHALL SYNAPTICS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, PUNITIVE, OR
# CONSEQUENTIAL DAMAGES ARISING OUT OF OR IN CONNECTION WITH THE USE
# OF THE INFORMATION CONTAINED IN THIS DOCUMENT, HOWEVER CAUSED AND
# BASED ON ANY THEORY OF LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, AND EVEN IF SYNAPTICS WAS
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. IF A TRIBUNAL OF
# COMPETENT JURISDICTION DOES NOT PERMIT THE DISCLAIMER OF DIRECT
# DAMAGES OR ANY OTHER DAMAGES, SYNAPTICS' TOTAL CUMULATIVE LIABILITY
# TO ANY PARTY SHALL NOT EXCEED ONE HUNDRED U.S. DOLLARS.

include(${CMAKE_CURRENT_SOURCE_DIR}/../../../doc-template/cmake/SynapticsThemeBuild.cmake)

# Generate sphynx documentation (based on doxygen output)
set(DOC_BUILD_DIR ${CMAKE_CURRENT_BINARY_DIR}/sphinx)
set(GENERATED_DOC ${DOC_BUILD_DIR}/latex/synapmodelimportandquantization.pdf)
file(GLOB DOC_SOURCES *.txt *.py *.rst *.yml
#    ${CMAKE_CURRENT_SOURCE_DIR}/../../toolkit/pysynap/requirements.txt
#    ${CMAKE_SOURCE_DIR}/models/test_report*.rst
)

synaptics_theme_build(
    DOC_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}
    BREATHE_PROJECTS "{ \"synap\": \"${DOXY_OUTPUT_DIR}/xml\" }"
    DOC_BUILD_DIR ${DOC_BUILD_DIR}
    DEPENDENCIES ${DOC_SOURCES} ${GENERATED_DOXY}
    GENERATED_DOCUMENT ${GENERATED_DOC}
)
add_custom_target(doc_wp_quant ALL DEPENDS ${GENERATED_DOC})

install(FILES ${GENERATED_DOC} DESTINATION doc RENAME SyNAP_ModelImport.pdf)

